# v0.1 implementation plan

Audience: document-tool maintainers and RAG developers who need small reproducible
Arabic PDF extraction cases when upgrading engines. Independent early-stage project;
no affiliation, adoption, or accuracy claims.

## Scope
Eight original synthetic text-layer PDFs, independently authored logical ground truth,
explicit token/order expectations, offline deterministic evaluators, optional Docling
and pypdf adapters, saved-output evaluation, run comparison, JSON and escaped portable
HTML. CPU sufficient. No models trained, scanned OCR matrix, paid APIs, dashboard,
publishing, pushing, or upstream issue posting.

## Architecture and format
Python 3.11+, src layout. Packaged data contains manifest.json, font/license, PDFs,
and UTF-8 source text. Manifest specifies ID, tags, pages, expected logical text,
ordered phrases, identifiers, numbers, provenance, license, generation instructions.
fpdf2 uses HarfBuzz shaping and bidi handling; never manually reverse strings.
Raw extraction is retained. NFC and optional whitespace collapse are explicit;
punctuation, digits, presentation forms and word order are never repaired.
Strict comparison is always reported separately. Normalized mode determines the
text gate. Phrase and exact token checks remain additional gates.

CLI: fixtures generate/verify; evaluate saved JSON; run engine; compare runs;
report JSON to HTML. Exit 0 pass, 1 failed expectation/regression, 2 infrastructure,
input error or skipped extraction. ERROR and SKIPPED never pass.

## Milestones, commits, acceptance
1. Scope/packaging: valid TOML, import and compile checks.
2. Corpus: eight PDFs and sources, hashes/provenance, render and visually inspect.
3. Evaluator: positive controls and deliberate mutations cover reversal, tokens,
   whitespace, empty/error output, correction and missing phrases.
4. Engines: current Docling API, exact runtime versions/config, actual attempted
   run with honest blocker evidence; optional real lightweight extraction.
5. CLI/reporting: end-to-end commands, regression/improvement detection, escaping.
6. Delivery: offline tests, lint, typing, build, fresh installation, quickstart,
   CI, results/status/roadmap and pinned integration example.

Each substantive commit follows its relevant checks. Full verification:
`python -m pytest -q`, `python -m ruff check .`, `python -m mypy src`,
`python -m build`, fresh venv wheel installation and installed CLI quickstart.
Model downloads never occur in default tests. Preserve existing MIT license.

## Research reviewed 2026-10-24
https://github.com/docling-project/docling/issues/1938 is closed; human maintainer
requested a current version and reproducer after no response. Closure is not proof
of a fix. Historical dosubot explanations are bot suggestions, not verified facts.
https://github.com/docling-project/docling/issues/3021 discusses scanned OCR;
the author challenges bot advice. Not a demonstrated current text-layer bug.
https://docling-project.github.io/docling/concepts/OCR/ describes current engine
and language choices. v0.1 disables OCR; no inference about scanned performance.
https://github.com/Antonhansel/arabic-ocr-bench evaluates multiple engines/models
and real scans. Our intended distinction is tiny original diagnostic cases and
version-to-version contract findings, not an engine leaderboard. The distinction
is a scope comparison, not a claim that other tools lack regression capabilities.
Generator reference: https://py-pdf.github.io/fpdf2/TextShaping.html.
