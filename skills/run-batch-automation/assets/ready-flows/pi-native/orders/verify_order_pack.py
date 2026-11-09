"""Independent business contract checker; does not import the builder."""
import csv
import json
import pathlib
import re
import sys
from collections import defaultdict


def verify(folder, source=None):
    from openpyxl import load_workbook
    from docx import Document
    checks = []
    def check(name, condition):
        checks.append({'check': name, 'pass': bool(condition)})
    with (pathlib.Path(source) if source is not None else folder/'orders.csv').open(encoding='utf-8-sig', newline='') as f:
        original = list(csv.DictReader(f))
    amounts = [int(r['amount_cents'])*int(r['quantity']) for r in original]
    indices = sorted(range(len(original)), key=lambda i: (-amounts[i], original[i]['order_id']))
    with (folder/'details.csv').open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        check('exact detail columns', reader.fieldnames == ['row_id','order_id','customer','amount_cents','quantity','total_cents'])
        details = list(reader)
    expected = [{**original[i], 'total_cents': str(amounts[i])} for i in indices]
    check('all rows exact and sorted including refunds duplicates and zero', details == expected)
    grouped = defaultdict(int)
    for r, amount in zip(original, amounts):
        grouped[r['customer']] += amount
    summary = json.loads((folder/'summary.json').read_text(encoding='utf-8-sig'))
    check('summary schema', set(summary) == {'row_count','total_cents','by_customer'})
    check('row count', summary.get('row_count') == len(original))
    check('grand total exact integer', type(summary.get('total_cents')) is int and summary['total_cents'] == sum(amounts))
    check('customer totals', summary.get('by_customer') == dict(grouped))
    text = Document(folder/'report.docx')
    body = '\n'.join(p.text for p in text.paragraphs)
    check('report title', '订单经营日报' in body)
    check('report row count and total', str(len(original)) in body and str(sum(amounts)) in body)
    cells = [c.text for t in text.tables for r in t.rows for c in r.cells]
    check('report all customer rows', all(k in cells and str(v) in cells for k,v in grouped.items()))
    formulas = load_workbook(folder/'ledger.xlsx', data_only=False)
    values = load_workbook(folder/'ledger.xlsx', data_only=True)
    check('required workbook sheets', formulas.sheetnames == ['Orders','Summary'])
    fs, vs = formulas['Orders'], values['Orders']
    check('workbook detail shape', fs.max_row == len(original)+1 and fs.max_column == 6)
    check('workbook headers', [fs.cell(1,c).value for c in range(1,7)] == ['row_id','order_id','customer','amount_cents','quantity','total_cents'])
    check('workbook preserves identifiers text', all(fs.cell(j+2,1).value == row['row_id'] and fs.cell(j+2,2).value == row['order_id'] for j,row in enumerate(expected)))
    check('workbook numeric inputs', all(fs.cell(j+2,4).value == int(row['amount_cents']) and fs.cell(j+2,5).value == int(row['quantity']) for j,row in enumerate(expected)))
    check('workbook row formulas', all(re.sub(r'\$|\s','',str(fs.cell(j+2,6).value)).upper() == f'=D{j+2}*E{j+2}' for j in range(len(expected))))
    check('workbook row cached results', all(vs.cell(j+2,6).value == int(row['total_cents']) for j,row in enumerate(expected)))
    ss, sv = formulas['Summary'], values['Summary']
    check('workbook grouped labels', [ss.cell(j+2,1).value for j in range(len(grouped))] == sorted(grouped))
    def canonical(formula):
        return re.sub(r"[\$\s']", '', str(formula)).upper()
    def valid_group_formula(j, customer):
        actual = canonical(ss.cell(j+2,2).value)
        exact = canonical(f'=SUMPRODUCT(--EXACT(Orders!C2:C{len(original)+1},A{j+2}),Orders!F2:F{len(original)+1})')
        if actual == exact:
            return True
        # Preserve the historical ordinary-name contract. Require EXACT for
        # wildcard/operator/numeric criteria and case-insensitive collisions.
        ordinary = not any(c in customer for c in '*?~') and customer[:1] not in '<>='
        ordinary = ordinary and not re.fullmatch(r'[+-]?[0-9.]+', customer)
        ordinary = ordinary and sum(k.casefold() == customer.casefold() for k in grouped) == 1
        legacy = canonical(f'=SUMIF(Orders!C2:C{len(original)+1},A{j+2},Orders!F2:F{len(original)+1})')
        return ordinary and actual == legacy
    check('workbook SUMIF formulas', all(valid_group_formula(j,k) for j,k in enumerate(sorted(grouped))))
    check('workbook grouped cached results', all(sv.cell(j+2,2).value == grouped[k] for j,k in enumerate(sorted(grouped))))
    check('workbook total formula and cache', ss.cell(len(grouped)+2,1).value == 'Total' and canonical(ss.cell(len(grouped)+2,2).value) == canonical(f'=SUM(B2:B{len(grouped)+1})') and sv.cell(len(grouped)+2,2).value == sum(amounts))
    return {'pass': all(c['pass'] for c in checks), 'checks': checks, 'count': len(checks)}


if __name__ == '__main__':
    try:
        result = verify(pathlib.Path(sys.argv[1]).resolve(strict=True))
    except Exception as exc:
        result = {'pass': False, 'error': f'{type(exc).__name__}: {exc}'}
    print(json.dumps(result, ensure_ascii=True))
    sys.exit(0 if result['pass'] else 1)
