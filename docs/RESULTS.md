# Actual results

2026-10-24, Windows, Python 3.11.4. Independent synthetic corpus, eight PDFs,
nine pages. Current measurements do not establish general Arabic accuracy or
reproduce any particular upstream issue attachment.

## pypdf 6.21.2, real text extraction
`arabic-pdf-kit run --engine pypdf --output evidence/pypdf.json`

PASS 0, FAIL 8, ERROR 0, SKIPPED 0; exit 1. Raw output and per-check findings
are in evidence/pypdf.json. All eight differ in logical text/order. Some Latin
identifiers and numbers survive; token presence alone is not proof of reading
order. No extracted text was reversed, reshaped or repaired to change scores.

## Fixture inspection
All nine rendered pages inspected using PyMuPDF 1.26.7 at detailed scale.
Arabic joins and paragraph/page order are legible; mixed Latin identifiers,
both digit systems and the ISO date display correctly. An initial date rendering
reordered date components; explicit LTR embeddings in generator input fixed it
before final corpus hashes and evidence were recorded. No ground truth changed.
Rendering tool is only used for visual QA, not as benchmark ground truth.

## Evaluator controls
22 offline tests passed at engine milestone, including positive controls and
deliberate synthetic corruptions. Mutations are not observed engine failures.
Docling installation/run evidence will be added during final verification.
