#!/usr/bin/env python3
"""Read-only lookup of registered batch-automation recipes; never execute one."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import sys
import unicodedata

DEFAULT_REGISTRY = Path(__file__).resolve().parent.parent / 'references' / 'recipes.json'
GENERIC = {'批量', '自动化', '批量自动化', 'batch', 'batches', 'automation',
           'automate', 'automated', 'automatic', 'batch automation'}
FIELDS = ('id', 'title', 'category', 'routing_class', 'verification', 'reference', 'invocation')
LOCAL_CLASSES = {'existing_recipe', 'official_native',
                 'existing_capability_route', 'official_native_recipe', 'captured_candidate'}
DEFAULT_LEARNED = (Path('C:/Users/A/Documents/DSH-Workspace/automation-flow-library/recipes.json')
                   if os.name == 'nt' else None)


def normalize(text):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', text).casefold()).strip()


def informative(text):
    clean = normalize(text)
    compact = re.sub(r'[\W_]+', '', clean)
    return bool(compact) and clean not in GENERIC and compact not in {
        re.sub(r'[\W_]+', '', word) for word in GENERIC}


def contains(text, term):
    """Chinese phrases use substring matching; ASCII words keep boundaries."""
    text, term = normalize(text), normalize(term)
    if not term:
        return False
    if re.search(r'[\u3400-\u9fff]', term):
        return term in text
    return re.search(r'(?<![a-z0-9_])' + re.escape(term) + r'(?![a-z0-9_])', text) is not None


def load_registry(path):
    value = json.loads(path.read_text(encoding='utf-8'))
    rows = value.get('recipes') if isinstance(value, dict) else None
    if not isinstance(rows, list):
        raise ValueError('Registry must contain a recipes array')
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or not all(key in row for key in (*FIELDS, 'search_terms')):
            raise ValueError('Recipe is missing required metadata')
        if not all(isinstance(row[key], str) and row[key].strip()
                   for key in ('id', 'title', 'category', 'routing_class')):
            raise ValueError('Recipe identifiers and labels must be nonempty strings')
        if not isinstance(row['search_terms'], list) or not all(
                isinstance(term, str) for term in row['search_terms']):
            raise ValueError('Recipe search_terms must be a string array')
        platform = row.get('platform')
        if platform is not None and not isinstance(platform, str) and not (
                isinstance(platform, list) and all(isinstance(item, str) for item in platform)):
            raise ValueError('Recipe platform must be a string, string array, or null')
        if row.get('source_url') is not None and not isinstance(row['source_url'], str):
            raise ValueError('Recipe source_url must be a string or null')
        identity = normalize(row['id'])
        if identity in seen:
            raise ValueError('Registry contains duplicate recipe identifiers')
        seen.add(identity)
    return rows


def result_row(row, terms, score):
    return {**{key: row[key] for key in FIELDS},
            'platform': row.get('platform'), 'source_url': row.get('source_url'),
            'source_categories': row.get('source_categories'),
            'deployment': row['verification'].get('deployment', {'state': 'NOT_CONFIGURED'}),
            'matched_terms': terms,
            'score': score, 'scope_match_required': True}


def platform_names(row):
    value = row.get('platform')
    return value if isinstance(value, list) else [value] if isinstance(value, str) else []


def categories(rows, kind='workflow'):
    allowed = {'workflow': {'public_workflow'}, 'source': {'source_catalog'},
               'local': LOCAL_CLASSES, 'all': None}[kind]
    counts = Counter(row['category'] for row in rows if allowed is None or row['routing_class'] in allowed)
    return [{'category': category, 'count': count} for category, count in counts.items()]


def lookup(rows, query='', recipe_id=None, list_mode=False, include_reference=False, limit=3,
           kind='workflow', category=None, platform=None):
    eligible = [row for row in rows if include_reference or
                row['routing_class'] != 'historical_reference']
    if category is not None:
        eligible = [row for row in eligible if row['category'].strip() == category.strip()
                    or category.strip() in row.get('source_categories', [])]
    if platform is not None:
        needle = normalize(platform)
        eligible = [row for row in eligible if needle and any(
            needle in normalize(name) for name in platform_names(row))]
    # Explicit id bypasses the kind filter, while retaining history and scope filters.
    if recipe_id is not None:
        exact = [row for row in eligible if normalize(row['id']) == normalize(recipe_id)]
        return [result_row(exact[0], [exact[0]['id']], 1000)] if exact else []
    allowed = {'workflow': {'public_workflow'}, 'source': {'source_catalog'},
               'local': LOCAL_CLASSES, 'all': None}[kind]
    if allowed is not None:
        eligible = [row for row in eligible if row['routing_class'] in allowed]
    if list_mode:
        return [result_row(row, [], 0) for row in eligible[:limit]]
    wanted = normalize(query)
    if not wanted or not informative(wanted):
        filtered = category is not None or platform is not None or kind != 'workflow'
        return [result_row(row, [], 0) for row in eligible[:limit]] if filtered else []
    exact = [row for row in eligible if normalize(row['id']) == wanted]
    if exact:
        return [result_row(exact[0], [exact[0]['id']], 1000)]
    # Only literal metadata matches are eligible; no fuzzy or suggested fallback.
    tokens = re.findall(r'[a-z0-9][a-z0-9_-]*|[\u3400-\u9fff]+', wanted)
    tokens = [token for token in tokens if len(token) > 1 and informative(token)]
    ranked = []
    for index, row in enumerate(eligible):
        terms, seen_terms, score = [], set(), 0

        def matched(term, weight):
            nonlocal score
            key = normalize(term)
            if key not in seen_terms:
                seen_terms.add(key)
                terms.append(term)
                score += weight

        for term in row['search_terms']:
            if informative(term) and contains(wanted, term):
                matched(term, 30 + min(len(normalize(term)), 20))
        if informative(row['id']) and contains(wanted, row['id']):
            matched(row['id'], 100)
        if informative(row['title']) and contains(wanted, row['title']):
            matched(row['title'], 80)
        for token in tokens:
            if contains(row['title'], token) or contains(row['category'], token) or any(
                    contains(name, token) for name in platform_names(row)):
                matched(token, 15)
        if terms:
            ranked.append((score, index, result_row(row, terms, score)))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in ranked[:limit]]


def positive_limit(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError('--limit must be positive')
    return min(number, 10)


def main(argv=None):
    # Windows callers consume JSON bytes; keep the wire encoding independent
    # of the host console codepage (e.g. GBK).
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='strict')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='*', help='Literal Chinese or English keywords')
    parser.add_argument('--registry', type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument('--learned', type=Path, default=DEFAULT_LEARNED,
                        help='Merge completed-task candidate index; absent default is harmless')
    parser.add_argument('--limit', type=positive_limit, default=3,
                        help='Maximum results, default 3; capped at 10')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--id', dest='recipe_id', help='Exact registered recipe id')
    mode.add_argument('--list', action='store_true', dest='list_mode')
    mode.add_argument('--categories', action='store_true',
                      help='List every public-workflow category and its count')
    parser.add_argument('--kind', choices=('workflow', 'source', 'local', 'all'),
                        help='Registry kind; default workflow')
    parser.add_argument('--category', help='Exact category label')
    parser.add_argument('--platform', help='Case-insensitive platform substring')
    parser.add_argument('--include-reference', action='store_true')
    parser.add_argument('--ready', action='store_true',
                        help='Only workflows with recorded READY deployment; does not install or test dependencies')
    args = parser.parse_args(argv)
    try:
        rows = load_registry(args.registry)
        if args.learned is not None and args.learned.is_file():
            learned_value = json.loads(args.learned.read_text(encoding='utf-8'))
            learned = load_registry(args.learned)
            identities = {normalize(row['id']) for row in rows}
            if any(normalize(row['id']) in identities for row in learned):
                raise ValueError('Captured index must not replace a packaged recipe')
            rows.extend(learned)
            for row in rows:
                uses = learned_value.get('uses', {}).get(row['id'])
                if uses:
                    row['verification'] = {**row['verification'], 'recorded_uses': uses}
        if args.ready:
            rows = [row for row in rows
                    if row['verification'].get('deployment', {}).get('state') == 'READY']
        if args.categories:
            values = categories(rows, args.kind or 'workflow')
            print(json.dumps({'status': 'MATCH' if values else 'NO_MATCH',
                'scope_match_required': True, 'categories': values,
                'total_workflows': sum(value['count'] for value in values)}, ensure_ascii=False))
            return 0
        results = lookup(rows, query=' '.join(args.query), recipe_id=args.recipe_id,
                         list_mode=args.list_mode or (args.kind is not None and
                             not normalize(' '.join(args.query)) and args.recipe_id is None),
                         include_reference=args.include_reference,
                         limit=args.limit, kind=args.kind or ('all' if args.ready else 'workflow'), category=args.category,
                         platform=args.platform)
    except (OSError, ValueError, TypeError) as error:
        print(json.dumps({'status': 'REGISTRY_ERROR', 'error': str(error),
                          'scope_match_required': True, 'results': []}, ensure_ascii=False))
        return 2
    print(json.dumps({'status': 'MATCH' if results else 'NO_MATCH',
                      'scope_match_required': True, 'results': results}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
