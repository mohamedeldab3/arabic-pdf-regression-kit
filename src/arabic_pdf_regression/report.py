"""Portable escaped HTML and compatible run comparison."""

from __future__ import annotations

import html
import json
from typing import Any


def validate(run: dict[str, Any]) -> None:
    if run.get("schema_version") != 1 or not isinstance(run.get("results"), list):
        raise ValueError("Expected version 1 recorded run")
    if not isinstance(run.get("corpus_sha256"), str) or not isinstance(run.get("engine"), dict):
        raise ValueError("Missing run provenance")
    ids = []
    for row in run["results"]:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise ValueError("Invalid fixture result")
        ids.append(row["id"])
        if row.get("status") not in ("PASS", "FAIL", "ERROR", "SKIPPED"):
            raise ValueError("Invalid extraction status")
        if row.get("mode") not in ("strict", "nfc", "nfc-whitespace"):
            raise ValueError("Invalid comparison mode")
        if not isinstance(row.get("raw"), str) or not isinstance(row.get("expectations"), dict):
            raise ValueError("Invalid result text/expectations")
        if not isinstance(row["expectations"].get("expected"), str):
            raise ValueError("Missing expected text")
        checks = row.get("checks")
        if not isinstance(checks, dict) or set(checks) != {"strict", "normalized", "phrase_order", "identifiers", "numbers"}:
            raise ValueError("Invalid result checks")
        if any(value is not None and type(value) is not bool for value in checks.values()):
            raise ValueError("Invalid check values")
        if not isinstance(row.get("findings"), list) or not isinstance(row.get("differences"), list):
            raise ValueError("Invalid findings/differences")
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Empty or duplicate result IDs")


def render(run: dict[str, Any]) -> str:
    validate(run)
    def esc(value: Any) -> str:
        return html.escape(str(value), quote=True)

    sections = []
    for row in run["results"]:
        sections.append(
            f'<section><h2>{esc(row["id"])}: {esc(row["status"])}</h2>'
            f'<p>Mode: {esc(row["mode"])}</p><h3>Expected logical text</h3>'
            f'<pre dir="auto">{esc(row["expectations"]["expected"])}</pre>'
            f'<h3>Raw extraction (JSON string notation)</h3>'
            f'<pre dir="auto">{esc(json.dumps(row["raw"], ensure_ascii=False))}</pre>'
            f'<h3>Checks</h3><pre>{esc(json.dumps(row["checks"], indent=2))}</pre>'
            f'<h3>Findings and differences</h3><pre dir="auto">'
            f'{esc(json.dumps({"findings": row["findings"], "differences": row["differences"], "missing_content": row.get("missing_content", [])}, ensure_ascii=False, indent=2))}'
            f'</pre><details><summary>Full fixture expectations</summary><pre dir="auto">'
            f'{esc(json.dumps(row["expectations"], ensure_ascii=False, indent=2))}'
            '</pre></details></section>'
        )
    metadata = {k: v for k, v in run.items() if k != "results"}
    return ('<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'">'
            '<title>Arabic PDF regression report</title><style>'
            'body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:0 20px;color:#172b3a;background:#f5f7fa}'
            'section{border-top:2px solid #b6c7d6;padding:24px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;'
            'background:white;padding:16px;border:1px solid #dae1e8}h1,h2{color:#144b63}'
            '</style><h1>Arabic PDF regression report</h1><p>Independent synthetic corpus; '
            'not a general accuracy benchmark. Diff offsets refer to selected comparison text.</p>'
            f'<h2>Run metadata and reproduction argv</h2><pre>{esc(json.dumps(metadata, ensure_ascii=False, indent=2))}</pre>'
            + "".join(sections) + '</html>')


def compare(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    validate(before)
    validate(after)
    if before["corpus_sha256"] != after["corpus_sha256"]:
        raise ValueError("Cannot compare different corpus ground truth")
    old = {r["id"]: r for r in before["results"]}
    new = {r["id"]: r for r in after["results"]}
    if len(old) != len(before["results"]) or len(new) != len(after["results"]):
        raise ValueError("Duplicate result IDs")
    regressions, improvements, incomparable = [], [], []
    for fixture_id in sorted(old.keys() | new.keys()):
        a, b = old.get(fixture_id), new.get(fixture_id)
        if a is None or b is None:
            incomparable.append({"id": fixture_id, "reason": "Fixture set changed"})
            continue
        if a["mode"] != b["mode"] or a["expectations"] != b["expectations"]:
            raise ValueError("Cannot compare different modes/expectations")
        if a.get("pdf_sha256") != b.get("pdf_sha256"):
            raise ValueError("Cannot compare different PDF bytes")
        if a["status"] in ("ERROR", "SKIPPED") or b["status"] in ("ERROR", "SKIPPED"):
            incomparable.append({"id": fixture_id, "reason": "ERROR/SKIPPED is not quality evidence"})
            continue
        for key in a["checks"]:
            if a["checks"][key] is True and b["checks"][key] is False:
                regressions.append({"id": fixture_id, "check": key})
            elif a["checks"][key] is False and b["checks"][key] is True:
                improvements.append({"id": fixture_id, "check": key})
    return {"schema_version": 1, "before_engine": before["engine"], "after_engine": after["engine"],
            "regressions": regressions, "improvements": improvements, "incomparable": incomparable,
            "exit_code": 2 if incomparable else int(bool(regressions))}
