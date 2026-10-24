"""Deterministic diagnostics; raw text is never repaired."""

from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher
from typing import Any

MODES = ("strict", "nfc", "nfc-whitespace")


def normalize(text: str, mode: str) -> str:
    if mode not in MODES:
        raise ValueError(f"Unknown comparison mode: {mode}")
    if mode == "strict":
        return text
    text = unicodedata.normalize("NFC", text)
    return " ".join(text.split()) if mode == "nfc-whitespace" else text


def token_present(token: str, text: str) -> bool:
    # Unicode word boundaries prevent 123 passing inside 91234 or ID-1 in ID-12.
    # Adjacent punctuation is allowed; a digit after decimal/date separators is not.
    pattern = r"(?<![\w-])(?<!\d[.,/])" + re.escape(token) + r"(?![\w-]|[.,/]\d)"
    return re.search(pattern, text) is not None


def evaluate(fixture: dict[str, Any], raw: str = "", *, mode: str = "nfc-whitespace",
             error: str | None = None, skipped: bool = False) -> dict[str, Any]:
    expected = fixture["expected"]
    target, actual = normalize(expected, mode), normalize(raw, mode)
    checks: dict[str, bool | None] = {
        "strict": expected == raw, "normalized": target == actual,
        "phrase_order": None, "identifiers": None, "numbers": None,
    }
    findings: list[dict[str, Any]] = []
    if error or skipped:
        status = "ERROR" if error else "SKIPPED"
        findings.append({"kind": status.lower(), "detail": error or "Engine not run"})
    else:
        if not raw.strip():
            findings.append({"kind": "empty", "detail": "No extracted content"})
        if target != actual:
            findings.append({"kind": "text", "detail": "Selected text comparison differs"})
        cursor = 0
        checks["phrase_order"] = True
        for phrase in fixture["phrases"]:
            needle = normalize(phrase, mode)
            offset = actual.find(needle, cursor)
            if offset < 0:
                checks["phrase_order"] = False
                findings.append({"kind": "phrase", "expected": phrase,
                                 "detail": "Missing or out of logical order"})
            else:
                cursor = offset + len(needle)
        for key in ("identifiers", "numbers"):
            checks[key] = True
            for token in fixture[key]:
                if not token_present(token, raw):
                    checks[key] = False
                    findings.append({"kind": key, "expected": token,
                                     "detail": "Exact token absent"})
        status = "FAIL" if findings else "PASS"
    differences = [
        {"kind": tag, "expected_span": [i, j], "actual_span": [a, b],
         "expected": target[i:j], "actual": actual[a:b]}
        for tag, i, j, a, b in SequenceMatcher(None, target, actual, autojunk=False).get_opcodes()
        if tag != "equal"
    ]
    missing_content = [d for d in differences
                       if d["kind"] in ("delete", "replace") and str(d["expected"]).strip()]
    return {"id": fixture["id"], "tags": fixture["tags"], "status": status,
            "expectations": fixture, "raw": raw, "mode": mode, "checks": checks,
            "findings": findings, "differences": differences, "missing_content": missing_content}


def exit_code(results: list[dict[str, Any]]) -> int:
    if not results or any(r["status"] in ("ERROR", "SKIPPED") for r in results):
        return 2
    return int(any(r["status"] == "FAIL" for r in results))
