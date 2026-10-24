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
35 offline tests passed in final verification, including positive controls and
deliberate synthetic corruptions. Mutations are not observed engine failures.
Actual CLI controls in evidence/synthetic-*.json:
- Authored positive control: 8 PASS, exit 0.
- Deliberately reversed words in one fixture: 7 PASS, 1 FAIL, exit 1.
- Comparing positive to mutation: 3 check regressions, exit 1.
- Comparing mutation to positive: 3 check improvements, exit 0.
- pypdf self-comparison: no regressions/improvements/incomparables, exit 0.

## Docling 2.142.1: infrastructure blocker, not Arabic accuracy

Installed in isolated .venv-docling; exact resolved dependencies are recorded in
evidence/docling-environment.txt. CPU, OCR false, table structure false. Two real
network-enabled smoke attempts on arabic-only reached the layout-model download
but left zero-byte incomplete weight files. Both were interrupted after stalling;
the second used HF_HUB_DISABLE_XET=1 and HF_HUB_DOWNLOAD_TIMEOUT=15. No complete
network-enabled extraction result was produced or counted.

A subsequent offline cache verification produced evidence/docling-smoke.json
and its HTML report: **0 PASS, 0 FAIL, 1 ERROR, 0 SKIPPED**, exit 2. Seven other
fixtures were not selected for Docling. This is infrastructure evidence, not an
engine benchmark. HF_HUB_OFFLINE=1 is explicitly recorded; it was set to make the
missing-artifact condition fail promptly, not to characterize online behavior.

Actual error: IncompleteSnapshotError, missing model.safetensors in
docling-project/docling-layout-heron, revision main resolved to commit
8f39ad3c0b4c58e9c2d2c84a38465abf757272d8. No claim about current Arabic behavior
in Docling or historical issue reproduction follows from this failed run.

Reproduce the offline check after a partial cache exists (PowerShell):
```powershell
$env:HF_HUB_OFFLINE='1'
.venv-docling/Scripts/python -m arabic_pdf_regression.cli run --engine docling --ids arabic-only --output tmp/docling-cache-check.json
```

To complete the missing real run, unset offline mode and provide network access to
the public layout weights (no API key required):
```powershell
Remove-Item Env:HF_HUB_OFFLINE -ErrorAction SilentlyContinue
.venv-docling/Scripts/python -m arabic_pdf_regression.cli run --engine docling --output tmp/docling-full.json --html tmp/docling-full.html
```
For a new environment first install the built wheel with its [docling] extra.
If the public model host remains inaccessible, preserve ERROR and do not replace
it with mocked extraction results.

## Verification actually performed

| Command | Observed result |
| --- | --- |
| `python -m pytest -q --basetemp tmp/pytest-release-final` | 35 passed |
| `python -m ruff check src tests tools examples` | All checks passed |
| `python -m mypy src` | No issues in 7 source files |
| `python -m build` | Wheel and source distribution built |
| Fresh venv, install wheel + pypdf==6.21.2 | Installed successfully |
| `python tools/verify_installed.py --python .venv-clean/Scripts/python.exe` | 6 console commands passed outside checkout |
| `python examples/run_subset.py` | 3 known FAIL observations, baseline comparison exit 0 |
| `fixtures generate --output tmp/regenerated` + SHA-256 comparison | All 8 PDFs byte-identical to committed corpus |

Generator stack: fpdf2 2.8.9, uharfbuzz 0.57.0, fonttools 4.67.0. The final test
run used a workspace-local temporary directory and had no warnings. Earlier
pytest runs emitted Windows temporary-directory cleanup warnings while still
passing. A first editable install with --no-build-isolation failed against an old
global setuptools; the documented default isolated build/install succeeded.

Browser preview QA could not connect to the browser tool. HTML generation,
escaping, metadata, and round-trip commands were tested; interactive browser
inspection is not claimed. PDF visual inspection was completed independently;
see evidence/corpus-contact-sheet.png. Hosted CI and Linux/macOS were not run.
