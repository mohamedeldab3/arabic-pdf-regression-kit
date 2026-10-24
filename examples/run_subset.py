"""Pinned integration example: compare real extraction to committed observations.

Run from repository root after installing the built 0.1.0 wheel and pypdf 6.21.2.
Known fixture failures are retained; only new regressions fail this baseline gate.
"""

import json
from importlib.metadata import version
from pathlib import Path

from arabic_pdf_regression.evaluate import exit_code
from arabic_pdf_regression.report import compare
from arabic_pdf_regression.runs import run, write_json

if version("arabic-pdf-regression-kit") != "0.1.0" or version("pypdf") != "6.21.2":
    raise RuntimeError("Example requires kit 0.1.0 and pypdf 6.21.2")
ids = ["arabic-only", "invoice-id", "amount-date"]
baseline = json.loads(Path("evidence/pypdf.json").read_text(encoding="utf-8"))
baseline["results"] = [r for r in baseline["results"] if r["id"] in ids]
baseline["summary"] = {status: sum(r["status"] == status for r in baseline["results"])
                       for status in ("PASS", "FAIL", "ERROR", "SKIPPED")}
baseline["exit_code"] = exit_code(baseline["results"])
current = run("pypdf", "nfc-whitespace", ids, ["python", "examples/run_subset.py"])
write_json(Path("tmp/subset.json"), current)
comparison = compare(baseline, current)
write_json(Path("tmp/subset-comparison.json"), comparison)
print(json.dumps({"current_summary": current["summary"], "comparison_exit": comparison["exit_code"]}))
raise SystemExit(comparison["exit_code"])
