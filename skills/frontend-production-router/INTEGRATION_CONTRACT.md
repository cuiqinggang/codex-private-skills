# Integration Contract v1

## Clone layer to design-system layer

Required fields in `clone-analysis.json`:

- `contract_version`, `source_authorization`, `source_url_or_image`, `desktop_screenshot`, `mobile_screenshot`, `page_structure`, `colors`, `fonts`, `type_scale`, `spacing_scale`, `radii`, `shadows`, `components`, `breakpoints`, `motion`, `page_files`, `stack`, `known_defects`.

## Design-system layer response

Required fields in `design-system-result.json`:

- `contract_version`, `design_md`, `tokens`, `originalize`, `preserve`, `forbidden_brand_elements`, `component_rules`, `extension_rules`, `validator_status`.

## Orchestrator checks

- Required files exist and resolve beneath the declared work root.
- `contract_version` is `1.0`.
- `source_authorization` is explicit for exact clone work.
- No stage invokes `frontend-production-router` recursively.
- A page path has one owner and is not generated twice.
- Similarity claims include matched desktop/mobile screenshots, score, and deduction logic.

