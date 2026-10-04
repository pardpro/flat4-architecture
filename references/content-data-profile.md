# F4A Content / Data Profile

Use for ingestion, transformation, analytics, datasets, reports, publishing, search indexes, and content production pipelines.

## Boundaries

- Separate sources, ingestion, normalization, transformation, storage, analysis, and publication.
- Preserve source provenance, timestamps, licensing, and consent requirements.
- Make schemas, quality expectations, and ownership explicit.
- Keep raw data immutable where auditability or reprocessing matters.
- Treat generated content and inferred fields as derived data with recorded lineage.

## Reliability

- Make jobs idempotent or define duplicate handling.
- Define late, missing, malformed, and contradictory input behavior.
- Version schemas and transformations.
- Add reconciliation for counts, totals, and critical joins.
- Separate preview/draft content from approved publication.
- Define retention, deletion, and access controls.

## Evidence

- representative fixtures and data-quality tests;
- schema and migration records;
- lineage and provenance for published outputs;
- freshness, completeness, and error-rate monitoring;
- reproducible evaluation for AI extraction or generation;
- rollback or reprocessing procedure.
