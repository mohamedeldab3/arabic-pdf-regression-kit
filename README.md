# Arabic PDF Regression Kit

[![CI](https://github.com/mohamedeldab3/arabic-pdf-regression-kit/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/mohamedeldab3/arabic-pdf-regression-kit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An independent Python kit for reproducing Arabic and mixed
Arabic/English PDF text-extraction regressions. Eight tiny original fixtures make
word order, Latin identifiers, numbers, dates and page/paragraph order explicit.
This is a diagnostic harness, not an OCR model or a general accuracy benchmark.
No upstream affiliation or adoption is claimed.

**Recorded evidence:** Docling 2.142.1 and pypdf 6.21.1/6.21.2 have been run on
the corpus. The kit detects their violated expectations, preserves raw outputs,
and compares upgrade behavior. Core CI has passed on Windows and Ubuntu with
Python 3.11 and 3.12. [Results](docs/RESULTS.md) · [Changelog](CHANGELOG.md) ·
[Contributing](CONTRIBUTING.md).

## Quickstart (Python 3.11+)

From this source checkout, create and activate a virtual environment:

```powershell
python -m venv .venv
.venv/Scripts/Activate.ps1
python -m pip install ".[pypdf]"
arabic-pdf-kit fixtures verify
arabic-pdf-kit run --engine pypdf --output tmp/pypdf.json --html tmp/pypdf.html
```

On Linux/macOS activate with `source .venv/bin/activate`. The CLI and evaluator
have no required third-party dependencies; extractors/generation are extras.
The committed PDFs, source text, manifest and licensed font are included in wheels.

Actual observed pypdf 6.21.2 output on the committed corpus:

```json
{"PASS": 0, "FAIL": 8, "ERROR": 0, "SKIPPED": 0}
```

**Exit 1 is expected for this recorded baseline**: extraction ran successfully,
but violated logical-text expectations. This does not mean the kit installation
failed. Open `tmp/pypdf.html` to inspect expected/raw text and exact differences.
See [actual results](docs/RESULTS.md) and [recorded report](evidence/pypdf.html).

## Offline evaluator and other commands

The positive control is authored logical text, **not engine output**:

```sh
arabic-pdf-kit evaluate examples/positive-control.json --output tmp/control.json --html tmp/control.html
arabic-pdf-kit report tmp/pypdf.json --html tmp/report.html
arabic-pdf-kit compare evidence/pypdf.json tmp/pypdf.json --output tmp/comparison.json
python -m pip install ".[fixtures]"
arabic-pdf-kit fixtures generate --output tmp/regenerated
```

Positive control: 8 PASS, exit 0. A saved-output file has `schema_version: 1`,
optional engine metadata and an `outputs` mapping from fixture ID to `{"raw": "..."}`
or `{"error": "..."}`. Missing IDs are SKIPPED; unknown IDs are input errors.
Engine runs can select a subset using `--ids arabic-only invoice-id amount-date`.

Exit codes: **0** all required checks passed (or report generation succeeded);
**1** violated expectation or comparison regression; **2** input/infrastructure
error, extraction ERROR, SKIPPED output, or incomparable runs. Never count
ERROR/SKIPPED as successful extraction. `report` only renders an existing artifact;
its exit code describes rendering, and the original run exit is visible inside it.

## What the checks mean

- Strict text equality is always recorded, including whitespace and punctuation.
- `--mode strict`, `nfc`, or default `nfc-whitespace` selects the text gate.
  The last mode applies NFC then collapses Unicode whitespace and trims edges.
  Phrase checks use the same selected normalization.
- Phrases must occur in their authored order, searched after the previous phrase.
- Identifiers and numeric tokens are checked exactly in raw output with boundaries.
  Arabic-Indic digits are not converted; punctuation/decimal/date changes remain.
- Empty output, engine errors, skipped output, missing/replaced content segments
  and character-offset differences are distinct diagnostics. Offsets refer to the
  selected comparison strings, not PDF geometry or necessarily the raw string.

HTML shows raw output in JSON string notation so control characters, carriage
returns and trailing whitespace remain visible. The JSON run retains exact raw text.

No reversal, reshaping, word sorting, bidi-control removal or punctuation deletion
is applied to engine output. Raw extraction is preserved. Comparisons require the
same corpus, PDF hashes, expectation set and comparison mode. They report each
check's regressions/improvements, even if both overall fixture statuses remain
FAIL. ERROR/SKIPPED and differing fixture sets are incomparable (exit 2).
Comparison does not claim statistical significance or compare general accuracy.

## Docling: optional real integration

```sh
python -m pip install ".[docling]"
arabic-pdf-kit run --engine docling --output tmp/docling.json --html tmp/docling.html
```

Pinned Docling 2.142.1 uses its supported DocumentConverter/PdfFormatOption API,
standard PDF pipeline, CPU, OCR disabled and table structure disabled. Standard
layout processing may still download model weights; initial execution needs
network/model artifacts. Default tests never load Docling or fetch models.
See [results and blockers](docs/RESULTS.md) for the actual run, separately from
synthetic evaluator tests. We do not claim the historical issue examples have
been reproduced or fixed.

Recorded Docling 2.142.1 extraction completed on all eight fixtures: **0 PASS,
8 FAIL, 0 ERROR, 0 SKIPPED**. The layout-weight download was recovered using the
pinned public artifact and verified SHA-256; extraction then ran from the complete
local cache. [Raw run](evidence/docling-2.142.1.json) ·
[HTML report](evidence/docling-2.142.1.html). These are contract failures on this
specific corpus, not a general Arabic accuracy score or a reproduction of an
upstream issue attachment.

## Development and CI integration

```sh
python -m pip install -e ".[dev,pypdf,fixtures]"
python -m pytest -q
python -m ruff check src tests tools examples
python -m mypy src
python -m build
python examples/run_subset.py
```

The [pinned subset integration](examples/run_subset.py) requires kit 0.1.0 and
pypdf 6.21.2 and compares three fixtures against recorded observations. It exits
0 when the known failures are unchanged; their FAIL status stays visible. For
another project, vendor the built `arabic_pdf_regression_kit-0.1.0-py3-none-any.whl`,
the example and its baseline, then install that exact wheel plus `pypdf==6.21.2`.
No PyPI release currently exists. A package-name-only install is not a supported
installation instruction for this unpublished project.
Copy [this workflow example](examples/ci-subset.yml) into a downstream project
after vendoring the wheel, subset script and baseline as listed in its header.

Clean-wheel verification (Windows; use `.venv-clean/bin/python` on Unix):

```powershell
python -m venv .venv-clean
.venv-clean/Scripts/python -m pip install dist/arabic_pdf_regression_kit-0.1.0-py3-none-any.whl pypdf==6.21.2
python tools/verify_installed.py --python .venv-clean/Scripts/python.exe
```

The verifier exercises six console commands outside the checkout with PYTHONPATH
removed. The [CI workflow](.github/workflows/ci.yml) runs Python 3.11/3.12 on
Windows/Linux. [Verified hosted matrix run](https://github.com/mohamedeldab3/arabic-pdf-regression-kit/actions/runs/40048373609).

## Limits and provenance

Synthetic text-layer cases do not establish real-world Arabic/OCR accuracy.
Presence of a token does not establish its reading order. No scanned OCR, tables,
columns, arbitrary user-document upload command, CER/WER leaderboard, or general
Arabic extraction solution is included. Rendering controls are added only in PDF
generation; expected logical text is independently authored and kept separate.
The font/renderer itself can influence extraction; these are specific PDF contracts.

Original corpus/code: existing MIT license. Noto Naskh Arabic: SIL OFL 1.1, bundled
with attribution. [Corpus details](docs/CORPUS.md), [related work](docs/RELATED_WORK.md),
[contributing](CONTRIBUTING.md), [roadmap](docs/ROADMAP.md), [status](docs/STATUS.md).

