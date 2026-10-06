"""HIPE v0.3.4 R4: offline, restricted SQLite categorical-literal binder.

Not a general SQL validator and not part of the HIPE runtime. SQLite prepares
SQL against an empty schema first. A bounded token/scope adapter then resolves
direct base-column/string predicates; ambiguous or unsupported bindings stop.
No task IDs, answer rows, network calls, or global table-name guessing.
"""
from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from typing import Iterable, Mapping


class AuditError(ValueError):
    """Cannot certify this binding; caller must stop, never silently pass."""


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    depth: int


_TOKEN = re.compile(
    r"(?P<WS>\s+)|(?P<COMMENT>--[^\n]*(?:\n|$)|/\*.*?\*/)|"
    r"(?P<STR>'(?:[^']|'')*')|(?P<QUOTED>\"(?:[^\"]|\"\")*\"|`(?:[^`]|``)*`|\[[^\]]*\])|"
    r"(?P<ID>[A-Za-z_][A-Za-z_0-9$]*)|(?P<NUM>\d+(?:\.\d+)?)|"
    r"(?P<OP><>|!=|==|<=|>=|=|<|>)|(?P<PUNCT>[(),.;*+/%|~&!-])",
    re.DOTALL,
)
_KEYWORDS = set("SELECT FROM JOIN LEFT RIGHT FULL INNER OUTER CROSS NATURAL ON USING WHERE GROUP BY HAVING ORDER LIMIT OFFSET WINDOW UNION INTERSECT EXCEPT AS INDEXED NOT INDEX WITH RECURSIVE ASC DESC AND OR IN IS LIKE GLOB REGEXP MATCH EXISTS WHEN THEN ELSE END CASE FILTER".split())


def _lex(sql: str) -> tuple[list[Token], dict[int, int]]:
    tokens: list[Token] = []
    pairs: dict[int, int] = {}
    stack: list[int] = []
    pos = depth = 0
    while pos < len(sql):
        match = _TOKEN.match(sql, pos)
        if match is None:
            raise AuditError(f"UNSUPPORTED_TOKEN_AT:{pos}")
        pos = match.end()
        kind, value = match.lastgroup, match.group()
        if kind in {"WS", "COMMENT"}:
            continue
        if kind == "STR":
            value = value[1:-1].replace("''", "'")
        elif kind == "QUOTED":
            q = value[0]
            value = value[1:-1].replace(q * 2, q) if q != '[' else value[1:-1]
        if value == ')' and kind == 'PUNCT':
            depth -= 1
            if not stack or depth < 0:
                raise AuditError("UNBALANCED_PARENTHESES")
            opening = stack.pop()
            pairs[opening] = len(tokens)
            pairs[len(tokens)] = opening
        tokens.append(Token(str(kind), value, depth))
        if value == '(' and kind == 'PUNCT':
            stack.append(len(tokens) - 1)
            depth += 1
    if stack:
        raise AuditError("UNBALANCED_PARENTHESES")
    return tokens, pairs


def _keyword(token: Token, word: str) -> bool:
    return token.kind == 'ID' and token.value.upper() == word


def _identifier(token: Token) -> bool:
    return token.kind in {'ID', 'QUOTED'}


def _catalog_and_prepare(sql: str, ddls: Iterable[str]) -> dict[str, set[str]]:
    """SQLite is the syntax/name-binding authority. No fixture data is loaded."""
    with sqlite3.connect(':memory:') as connection:
        for ddl in ddls:
            ddl_tokens, _ = _lex(ddl)
            if len(ddl_tokens) < 3 or not _keyword(ddl_tokens[0], 'CREATE') or not _keyword(ddl_tokens[1], 'TABLE'):
                raise AuditError('SCHEMA_REQUIRES_CREATE_TABLE_ONLY')
            connection.execute(ddl)
        names = [row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")]
        catalog = {}
        for name in names:
            quoted = '"' + name.replace('"', '""') + '"'
            catalog[name.casefold()] = {row[1].casefold() for row in connection.execute(f'PRAGMA table_info({quoted})')}
        allowed = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION, sqlite3.SQLITE_RECURSIVE}
        connection.set_authorizer(lambda action, _a, _b, _db, _source: sqlite3.SQLITE_OK if action in allowed else sqlite3.SQLITE_DENY)
        try:
            connection.execute('EXPLAIN ' + sql).fetchall()
        except sqlite3.Error as exc:
            raise AuditError('SQLITE_PREPARE_REJECTED:' + str(exc)) from exc
        return catalog


@dataclass
class Scope:
    start: int
    end: int
    depth: int
    sources: dict[str, str | None]


def extract_bindings(sql: str, schema: Iterable[str]) -> list[dict[str, object]]:
    """Return table/column/literal/operator/scope for direct string predicates.

    Supported: SELECT/CTE/subquery scopes, local physical table aliases, base
    columns, =/!=/<>/ordering comparisons, IN/NOT IN literal lists, correlated
    qualified/unqualified base columns where resolution is unambiguous.
    CTE/derived-table projected categorical columns, expression-derived column
    predicates, and unsupported lexical constructs are rejected, not guessed.
    Numeric thresholds, output literals, and function-format literals are not
    categorical-column requirements; existing R3 checks still cover their specs.
    """
    tokens, pairs = _lex(sql)
    if not tokens or not (_keyword(tokens[0], 'SELECT') or _keyword(tokens[0], 'WITH')):
        raise AuditError('SELECT_ONLY')
    catalog = _catalog_and_prepare(sql, schema)
    scopes: list[Scope] = []
    for i, token in enumerate(tokens):
        if _keyword(token, 'SELECT'):
            end = len(tokens)
            for j in range(i + 1, len(tokens)):
                t = tokens[j]
                if t.depth < token.depth or (t.depth == token.depth and ((t.kind == 'PUNCT' and t.value == ';') or any(_keyword(t, x) for x in ('UNION', 'INTERSECT', 'EXCEPT')))):
                    end = j
                    break
            scopes.append(Scope(i, end, token.depth, {}))
    if not scopes:
        raise AuditError('NO_SELECT_SCOPE')

    def owner(index: int) -> Scope:
        matches = [s for s in scopes if s.start <= index < s.end]
        if not matches:
            raise AuditError(f'NO_SCOPE:{index}')
        return max(matches, key=lambda s: s.start)

    # Conservatively distinguish CTE names from physical tables. A CTE that
    # shadows a physical table is not guessed, even in an unrelated scope.
    cte_names: set[str] = set()
    for i in range(1, len(tokens) - 1):
        if _keyword(tokens[i], 'AS') and tokens[i + 1].value == '(':
            prev = i - 1
            if tokens[prev].value == ')':
                prev = pairs[prev] - 1
            if prev >= 0 and _identifier(tokens[prev]):
                cte_names.add(tokens[prev].value.casefold())

    stops = {'WHERE', 'GROUP', 'HAVING', 'ORDER', 'LIMIT', 'WINDOW', 'UNION', 'INTERSECT', 'EXCEPT'}
    for scope in scopes:
        in_from = False
        for i in range(scope.start + 1, scope.end):
            t = tokens[i]
            if t.depth != scope.depth or owner(i) is not scope:
                continue
            if t.kind == 'ID' and t.value.upper() in stops:
                in_from = False
            is_source = _keyword(t, 'FROM') or _keyword(t, 'JOIN') or (in_from and t.value == ',')
            if not is_source:
                continue
            in_from = True
            j = i + 1
            if j >= scope.end:
                raise AuditError('MISSING_SOURCE')
            physical = None
            if tokens[j].value == '(':
                j = pairs[j] + 1
                default_alias = f'__derived_{i}'
            elif _identifier(tokens[j]):
                default_alias = tokens[j].value.casefold()
                j += 1
                if j < scope.end and tokens[j].value == '.':
                    if default_alias != 'main' or j + 1 >= scope.end or not _identifier(tokens[j + 1]):
                        raise AuditError('UNSUPPORTED_SCHEMA_QUALIFIER')
                    default_alias = tokens[j + 1].value.casefold()
                    j += 2
                if default_alias in catalog and default_alias not in cte_names:
                    physical = default_alias
            else:
                raise AuditError('UNSUPPORTED_SOURCE')
            if j < scope.end and _keyword(tokens[j], 'AS'):
                j += 1
                if j >= scope.end or not _identifier(tokens[j]):
                    raise AuditError('INVALID_SOURCE_ALIAS')
                alias = tokens[j].value.casefold()
            elif j < scope.end and _identifier(tokens[j]) and (tokens[j].kind == 'QUOTED' or tokens[j].value.upper() not in _KEYWORDS):
                alias = tokens[j].value.casefold()
            else:
                alias = default_alias
            if alias in scope.sources:
                raise AuditError('DUPLICATE_SOURCE_ALIAS:' + alias)
            scope.sources[alias] = physical

    def resolve(parts: list[str], index: int) -> tuple[str, str]:
        scope = owner(index)
        chain = sorted([s for s in scopes if s.start <= scope.start and scope.end <= s.end], key=lambda s: s.start, reverse=True)
        column = parts[-1].casefold()
        if len(parts) > 2:
            raise AuditError('UNSUPPORTED_COLUMN_QUALIFIER')
        if len(parts) == 2:
            qualifier = parts[0].casefold()
            for current in chain:
                if qualifier in current.sources:
                    table = current.sources[qualifier]
                    if table is None:
                        raise AuditError('DERIVED_COLUMN_BINDING_UNSUPPORTED:' + '.'.join(parts))
                    if column not in catalog[table]:
                        raise AuditError('COLUMN_NOT_IN_SOURCE:' + '.'.join(parts))
                    return table, column
            raise AuditError('QUALIFIER_NOT_FOUND:' + qualifier)
        for current in chain:
            if any(table is None for table in current.sources.values()):
                raise AuditError('UNQUALIFIED_COLUMN_WITH_UNKNOWN_SOURCE:' + column)
            candidates = [table for table in current.sources.values() if table is not None and column in catalog[table]]
            if len(candidates) == 1:
                return str(candidates[0]), column
            if len(candidates) > 1:
                raise AuditError('AMBIGUOUS_COLUMN:' + column)
        raise AuditError('COLUMN_NOT_FOUND:' + column)

    def column_left(index: int) -> list[str] | None:
        if index < 0:
            return None
        if tokens[index].value == ')':
            opening = pairs[index]
            # Only parentheses around one direct column, never function calls.
            if opening > 0 and _identifier(tokens[opening - 1]) and tokens[opening - 1].value.upper() not in _KEYWORDS:
                return None
            inside = tokens[opening + 1:index]
            if len(inside) == 1 and _identifier(inside[0]):
                return [inside[0].value]
            if len(inside) == 3 and _identifier(inside[0]) and inside[1].value == '.' and _identifier(inside[2]):
                return [inside[0].value, inside[2].value]
            return None
        if not _identifier(tokens[index]):
            return None
        parts = [tokens[index].value]
        j = index - 1
        while j >= 1 and tokens[j].value == '.' and _identifier(tokens[j - 1]):
            parts.insert(0, tokens[j - 1].value)
            j -= 2
        if j >= 0 and (_keyword(tokens[j], 'COLLATE') or tokens[j].value in {'+', '-', '*', '/', '|'}):
            return None
        return parts

    def column_right(index: int) -> list[str] | None:
        if index >= len(tokens) or not _identifier(tokens[index]):
            return None
        parts = [tokens[index].value]
        j = index + 1
        while j + 1 < len(tokens) and tokens[j].value == '.' and _identifier(tokens[j + 1]):
            parts.append(tokens[j + 1].value)
            j += 2
        if j < len(tokens) and (tokens[j].value in {'(', '+', '-', '*', '/', '|'} or _keyword(tokens[j], 'COLLATE')):
            return None
        return parts

    bindings: list[dict[str, object]] = []
    def add(parts: list[str] | None, literal: str, index: int, operator: str) -> None:
        if not parts:
            raise AuditError('NON_BASE_COLUMN_STRING_PREDICATE_UNSUPPORTED')
        table, column = resolve(parts, index)
        bindings.append({'table': table, 'column': column, 'literal': literal,
                         'operator': operator, 'scope_start_token': owner(index).start})

    for i, t in enumerate(tokens):
        if t.kind == 'OP' and 0 < i < len(tokens) - 1:
            left, right = tokens[i - 1], tokens[i + 1]
            if left.kind == right.kind == 'STR':
                continue  # Literal-to-literal, no database column semantics.
            if right.kind == 'STR':
                add(column_left(i - 1), right.value, i, t.value)
            elif left.kind == 'STR':
                add(column_right(i + 1), left.value, i, t.value)
        elif _keyword(t, 'IN') and i + 1 < len(tokens) and tokens[i + 1].value == '(':
            end = pairs[i + 1]
            inside = tokens[i + 2:end]
            if any(_keyword(x, 'SELECT') for x in inside):
                continue  # Its own SELECT scope is independently checked.
            strings = [x for x in inside if x.kind == 'STR']
            if not strings:
                continue
            if any(x.kind not in {'STR', 'NUM'} and x.value != ',' for x in inside):
                raise AuditError('NON_LITERAL_IN_LIST_UNSUPPORTED')
            not_in = i > 0 and _keyword(tokens[i - 1], 'NOT')
            parts = column_left(i - 2 if not_in else i - 1)
            for literal in strings:
                add(parts, literal.value, i, 'NOT IN' if not_in else 'IN')
        elif t.kind == 'ID' and t.value.upper() in {'LIKE', 'GLOB', 'REGEXP', 'MATCH', 'IS'}:
            j = i + 2 if i + 1 < len(tokens) and _keyword(tokens[i + 1], 'NOT') else i + 1
            if j < len(tokens) and tokens[j].kind == 'STR':
                raise AuditError('STRING_OPERATOR_UNSUPPORTED:' + t.value.upper())
    return bindings


def check_declarations(bindings: Iterable[Mapping[str, object]], declared: Mapping[str, Iterable[str]]) -> dict[str, object]:
    """Compare column-scoped permitted literals, not a global bag of strings.

    declared is an OFFLINE projection of existing R3 value_semantics:
    {'payments.status': ['success'], 'refunds.status': ['done']}.
    It must be constructed from the PUBLIC contract only, never from reference
    SQL or fixture data. Do not change the model input or the original contract.
    """
    normalized = {key.casefold(): set(values) for key, values in declared.items()}
    missing = []
    for item in bindings:
        key = f"{item['table']}.{item['column']}".casefold()
        if item['literal'] not in normalized.get(key, set()):
            missing.append({'column': key, 'literal': item['literal']})
    return {'status': 'PASS' if not missing else 'FAIL', 'missing': missing}


def extract_frozen_bindings(sql: str, schema: Iterable[str]) -> list[dict[str, object]]:
    """The only approved R3 integration entry point.

    Require an exact reference/schema pair from the fetched historical oracle.
    This prevents the restricted adapter from certifying arbitrary SQL. IDs do
    not select behavior: all approved inputs use the identical binding logic.
    """
    import json
    from pathlib import Path
    schema_list = list(schema)
    frozen = json.loads(Path(__file__).with_name('PRIVATE_REFERENCE_AUDIT.json').read_text(encoding='utf-8'))['cases']
    if not any(sql == item['reference'] and schema_list == item['schema'] for item in frozen):
        raise AuditError('REFERENCE_OR_SCHEMA_OUTSIDE_FROZEN_AUDIT_DOMAIN')
    return extract_bindings(sql, schema_list)
