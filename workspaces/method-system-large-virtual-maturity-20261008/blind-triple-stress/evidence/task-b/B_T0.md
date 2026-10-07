# B-T0 — INITIAL RELEASED EVIDENCE
TASK_ID=BLIND-B-OWID-ENERGY-20260910
SLICE=B-T0
RELEASE_PIN=2026-09-10

Goal: construct the pinned OWID Energy release candidate from source-side evidence without reading the final product.

Source families known to be in scope:
- Energy Institute statistics,
- Ember global/europe electricity data,
- U.S. EIA international energy data,
- historical energy/electricity reconstructions,
- OWID region/country/ISO definitions,
- population,
- Maddison GDP.

At T0:
- freeze provenance and exact versions before transformation;
- establish source schemas, units, keys, licensing/provenance and checksum strategy;
- do not access any fixed final owid_energy CSV/Parquet/Feather or final reconciliation values.
