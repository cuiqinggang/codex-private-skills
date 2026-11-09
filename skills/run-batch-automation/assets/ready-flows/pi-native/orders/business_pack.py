"""Parameterized order report over csv, XlsxWriter and python-docx.

Adapts the previously verified dsh-mature-20261025 Office example. No scheduler.
All writes are below an explicit output directory; invalid input fails before output.
"""
import argparse
import csv
import hashlib
import io
import json
import pathlib
import re

FIELDS = ['row_id', 'order_id', 'customer', 'amount_cents', 'quantity']
OUT_FIELDS = FIELDS + ['total_cents']


def load_rows(source):
    if source.stat().st_size > 16 * 1024 * 1024:
        raise ValueError('INPUT_EXCEEDS_16MIB')
    with source.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f, strict=True)
        if reader.fieldnames != FIELDS:
            raise ValueError('EXPECTED_EXACT_COLUMNS: ' + ','.join(FIELDS))
        rows = []
        for position, row in enumerate(reader):
            if None in row or any(row[k] is None for k in FIELDS):
                raise ValueError('MALFORMED_ROW')
            if any(not row[k].strip() for k in ['row_id', 'order_id', 'customer']):
                raise ValueError('EMPTY_IDENTIFIER')
            for k in ['amount_cents', 'quantity']:
                if not re.fullmatch(r'[+-]?[0-9]+', row[k]):
                    raise ValueError('INTEGER_REQUIRED: ' + k)
                row[k] = int(row[k])
            if row['quantity'] < 0:
                raise ValueError('NEGATIVE_QUANTITY')
            row['total_cents'] = row['amount_cents'] * row['quantity']
            # Excel's numeric precision is finite. Reject instead of rounding money.
            if any(abs(row[k]) > 999_999_999_999_999 for k in ['amount_cents', 'quantity', 'total_cents']):
                raise ValueError('EXCEL_EXACT_INTEGER_RANGE_EXCEEDED')
            rows.append(row)
    if not rows:
        raise ValueError('EMPTY_INPUT')
    rows.sort(key=lambda r: (-r['total_cents'], r['order_id']))
    grouped = {}
    for r in rows:
        grouped[r['customer']] = grouped.get(r['customer'], 0) + r['total_cents']
    summary = {'row_count': len(rows), 'total_cents': sum(r['total_cents'] for r in rows),
               'by_customer': dict(sorted(grouped.items()))}
    if abs(summary['total_cents']) > 999_999_999_999_999 or any(abs(v) > 999_999_999_999_999 for v in grouped.values()):
        raise ValueError('EXCEL_EXACT_INTEGER_RANGE_EXCEEDED')
    return rows, summary


def build(source, output, title):
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    import xlsxwriter
    rows, summary = load_rows(source)
    # Build everything in memory first. Input errors cannot leave partial output.
    csv_buffer = io.StringIO(newline='')
    writer = csv.DictWriter(csv_buffer, OUT_FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    book_buffer = io.BytesIO()
    book = xlsxwriter.Workbook(book_buffer, {'in_memory': True, 'strings_to_formulas': False, 'strings_to_urls': False})
    header = book.add_format({'bold': True, 'bg_color': '#193A55', 'font_color': '#FFFFFF', 'border': 1})
    integer = book.add_format({'num_format': '#,##0'})
    orders = book.add_worksheet('Orders')
    orders.freeze_panes(1, 0)
    orders.autofilter(0, 0, len(rows), len(OUT_FIELDS)-1)
    orders.set_column(0, 1, 14)
    orders.set_column(2, 2, 20)
    orders.set_column(3, 5, 20, integer)
    orders.write_row(0, 0, OUT_FIELDS, header)
    for index, row in enumerate(rows, 1):
        orders.write_row(index, 0, [row[k] for k in FIELDS])
        orders.write_formula(index, 5, f'=D{index+1}*E{index+1}', integer, row['total_cents'])
    totals = book.add_worksheet('Summary')
    totals.set_column(0, 0, 24)
    totals.set_column(1, 1, 24, integer)
    totals.write_row(0, 0, ['customer', 'total_cents'], header)
    for index, (customer, value) in enumerate(summary['by_customer'].items(), 1):
        totals.write_string(index, 0, customer)
        # Literal, case-sensitive names: SUMIF treats wildcard/operator-looking
        # names and case variants differently from the source's exact grouping.
        totals.write_formula(index, 1, f'=SUMPRODUCT(--EXACT(Orders!C2:C{len(rows)+1},A{index+1}),Orders!F2:F{len(rows)+1})', integer, value)
    final = len(summary['by_customer']) + 1
    totals.write_string(final, 0, 'Total')
    totals.write_formula(final, 1, f'=SUM(B2:B{final})', integer, summary['total_cents'])
    book.close()
    document = Document()
    section = document.sections[0]
    section.page_width, section.page_height = Inches(8.5), Inches(11)
    section.left_margin = section.right_margin = Inches(.8)
    for name in ['Normal', 'Title', 'Heading 1']:
        style = document.styles[name]
        style.font.name = 'Microsoft YaHei'
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), 'Microsoft YaHei')
    document.styles['Normal'].font.size = Pt(11)
    document.add_heading(title, 0)
    document.add_paragraph(f"本次共 {summary['row_count']} 条订单明细，合计 {summary['total_cents']} 分。重复订单号、退款和零金额明细均保留。")
    document.add_heading('客户汇总', 1)
    table = document.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    table.rows[0].cells[0].text, table.rows[0].cells[1].text = '客户', '合计金额 分'
    for customer, value in summary['by_customer'].items():
        cells = table.add_row().cells
        cells[0].text, cells[1].text = customer, str(value)
    document.add_paragraph('金额采用整数分计算。可编辑的逐行公式及客户汇总公式见随附 Excel。')
    doc_buffer = io.BytesIO()
    document.save(doc_buffer)
    output.mkdir(parents=True, exist_ok=True)
    artifacts = {'details.csv': csv_buffer.getvalue().encode('utf-8'),
                 'summary.json': json.dumps(summary, ensure_ascii=False, indent=2).encode('utf-8'),
                 'ledger.xlsx': book_buffer.getvalue(), 'report.docx': doc_buffer.getvalue()}
    for name, data in artifacts.items():
        (output/name).write_bytes(data)
    return {'status': 'CREATED_UNVERIFIED', 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'row_count': len(rows), 'total_cents': summary['total_cents'],
            'files': [str(output/name) for name in artifacts],
            'formula_cache': 'fresh integer arithmetic; not LibreOffice recalculation'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--title', default='订单经营日报')
    args = parser.parse_args()
    source, output = pathlib.Path(args.input).resolve(strict=True), pathlib.Path(args.out).resolve()
    receipt = build(source, output, args.title)
    from verify_order_pack import verify
    receipt['qa'] = verify(output, source)
    if not receipt['qa']['pass']:
        raise RuntimeError('OUTPUT_CONTRACT_FAILED: ' + json.dumps(receipt['qa']))
    receipt['status'] = 'CONTENT_ACCEPTED'
    print(json.dumps(receipt, ensure_ascii=True))
