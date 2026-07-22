#!/usr/bin/env python3
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--product-type', required=True)
    p.add_argument('--audience', default='general')
    p.add_argument('--overseas', action='store_true')
    p.add_argument('--tone', default='clear and trustworthy')
    p.add_argument('--stack', default='Next.js, TypeScript, Tailwind CSS')
    p.add_argument('--output', required=True)
    a=p.parse_args()
    routes=json.loads((ROOT/'catalog/use-case-map.json').read_text(encoding='utf-8'))
    archetypes={x['id']:x for x in json.loads((ROOT/'catalog/archetypes.json').read_text(encoding='utf-8'))}
    route=routes.get(a.product_type.lower(), routes['saas'])
    primary, secondary=archetypes[route['primary']], archetypes[route['secondary']]
    text=f'''# Project Design System\n\n## 1. Product Intent\nProduct type: {a.product_type}. Audience: {a.audience}. Market: {'overseas' if a.overseas else 'local or mixed'}. Tone: {a.tone}.\n\n## 2. Design Direction\nPrimary archetype: {primary['name']}. Supporting archetype: {secondary['name']}. Use the primary for structure and the supporting archetype only for emphasis. Avoid brand-specific signatures.\n\n## 3. Color Tokens\n- `--color-bg: #F7F8FA`\n- `--color-surface: #FFFFFF`\n- `--color-text: #111827`\n- `--color-muted: #667085`\n- `--color-primary: #3157D5`\n- `--color-danger: #B42318`\nMaintain WCAG AA contrast and never encode state by color alone.\n\n## 4. Typography\nUse `Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif`. Scale: 12, 14, 16, 20, 24, 32, 48px. Body is 16px/1.6; headings use 700 weight.\n\n## 5. Spacing and Shape\nSpacing scale: 4, 8, 12, 16, 24, 32, 48, 64px. Radius scale: 6, 10, 16px. Use one subtle shadow token and borders before shadows.\n\n## 6. Layout and Responsive Rules\nUse a 12-column desktop grid, 8-column tablet grid, and 4-column mobile grid. Breakpoints: 640, 768, 1024, 1280px. Verify 390x844 and 1440x900. No horizontal scroll. Touch targets are at least 44x44px.\n\n## 7. Components and States\nDefine button, input, navigation, card, table/list, dialog, toast, and skeleton. Each includes default, hover, focus, active, disabled, loading, empty, error, and success states.\n\n## 8. Accessibility\nUse semantic landmarks, keyboard order, visible focus, associated labels/errors, reduced-motion support, alt text, and AA contrast.\n\n## 9. Do / Don't and Originality\nDo use owned product names, original copy, legal icons, recomposed layouts, and project-specific components. Don't copy logos, trademarks, proprietary illustrations, restricted fonts, full source copy, or a reference site's complete composition.\n\n## 10. Technical Contract\nStack: {a.stack}. Keep design rules in this file; keep build/test instructions in AGENTS.md and business rules in product requirements.\n'''
    Path(a.output).write_text(text, encoding='utf-8')
    print(f'COMPOSE_RESULT=PASS primary={primary["id"]} secondary={secondary["id"]} output={Path(a.output).resolve()}')

if __name__=='__main__': main()

