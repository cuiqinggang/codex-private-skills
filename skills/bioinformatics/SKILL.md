---
name: bioinformatics
description: Use when this Windows Codex studio needs bioinformatics workflow planning or review for genomics, sequencing, variant calling, single-cell, metagenomics, computational biology, or biomedical data pipelines. Use as a Windows-safe planning and verification guide, not as permission to install large toolchains or process sensitive medical data without explicit scope.
---

# Bioinformatics Windows Studio

Use this skill for bioinformatics task planning, command review, data-layout checks, and reproducible workflow design on Windows.

## Boundaries

- Treat clinical, patient, genetic, and biomedical data as sensitive.
- Do not expose or upload private datasets.
- Do not install large toolchains, Conda environments, Docker images, cloud resources, or reference genomes without explicit task need and a reviewed plan.
- Prefer read-only inspection, manifest creation, and small sample dry-runs.

## Windows Studio Workflow

1. Classify the task: FASTQ/QC, alignment, variant calling, annotation, single-cell, metagenomics, statistics, visualization, or literature review.
2. Identify data location, file sizes, privacy level, and expected output.
3. Prefer existing project scripts or mature standard tools; verify availability before suggesting new installs.
4. For Windows, choose the appropriate runtime: native executable, Docker Desktop, WSL only if explicitly allowed, or cloud only after Stop Gate review.
5. Start with a tiny sample or dry-run and preserve logs.
6. Report commands, versions, input/output paths, and PASS/FAIL evidence.

## Verification

- PASS: reproducible plan or dry-run with versions, paths, and logs.
- FAIL: missing data scope, sensitive-data ambiguity, unreviewed install, or uncontrolled cloud upload.

