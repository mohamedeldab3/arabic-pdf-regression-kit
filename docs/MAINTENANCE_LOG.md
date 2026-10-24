# Maintenance log

## 2026-10-24: internal audit of numeric boundaries and recorded-run validation

Source: maintainer-initiated inspection and deliberate local test mutations.
No external complaint, reporter, adoption or upstream defect is implied.

### Finding 1: Arabic numeric separators caused false-positive token diagnostics

At base commit c681156, checking token `123` inside synthetic extracted text
`٩٬123` returned true. Likewise `١٢٣` was accepted inside `١٢٣٫٤`. Arabic
thousands (`U+066C`) and decimal (`U+066B`) separators were absent from boundary
checks. Overall text comparison still failed, but the numeric-preservation check
incorrectly reported that the expected token survived exactly.

Fix: include both separators in adjacent-number boundary checks, with Unicode
digits on either side. Keep Arabic comma punctuation (`U+060C`) accepted, preserve
raw text, and do not convert digit systems or remove punctuation.

### Finding 2: contradictory run metadata was accepted

A saved run containing eight PASS rows but a summary claiming zero PASS could be
rendered as HTML and used in comparisons. Invalid engine metadata could also be
written to a saved artifact. These findings were reproduced with deliberately
modified positive controls, not with an actual extractor benchmark.

Fix: validate exact status counts, integer summary values, and the expected exit
code before rendering or comparing. Reject booleans masquerading as numeric
schema versions/exit codes. Validate engine name/version before saved evaluation
writes an output. Malformed input returns exit 2. Valid FAIL, ERROR and SKIPPED
artifacts remain supported; these checks are consistency validation, not a
cryptographic authenticity guarantee or full recomputation of every check.

The subset CI example now recalculates counts and exit code after selecting its
three rows. This is required when deriving a subset from a recorded full run.

### Verification

- Before fixes: all 19 new targeted test cases failed.
- After fixes: all 19 targeted cases and the complete 54-test suite passed.
- Positive controls and actual correction checks prevent rejection of every input.
- Re-evaluated all 24 previously measured fixture outputs across Docling 2.142.1
  and pypdf 6.21.1/6.21.2: stored statuses/checks remain unchanged.
- Tests: `python -m pytest -q tests/test_maintenance_regressions.py` and full pytest.
- [Machine-readable evidence](../evidence/internal-maintenance-audit.json).

These entries document actual maintenance. An independent user's report can be
linked here later only if that report and its attribution actually exist.
