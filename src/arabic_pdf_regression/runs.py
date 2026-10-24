"""Run artifacts preserve raw extraction, environment and corpus identity."""

from __future__ import annotations

import platform
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import __version__, engines
from .corpus import DATA, digest, load_corpus
from .evaluate import evaluate, exit_code


def envelope(results: list[dict[str, Any]], engine: dict[str, Any],
             command: list[str]) -> dict[str, Any]:
    return {"schema_version": 1, "kit_version": __version__,
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "python": platform.python_version(), "platform": platform.platform(),
            "corpus_sha256": digest(DATA / "manifest.json"),
            "engine": engine, "reproduce_argv": command,
            "exit_code": exit_code(results),
            "summary": {s: sum(r["status"] == s for r in results)
                        for s in ("PASS", "FAIL", "ERROR", "SKIPPED")},
            "results": results}


def run(engine: str, mode: str, ids: list[str] | None,
        command: list[str]) -> dict[str, Any]:
    fixtures = load_corpus()
    if ids:
        unknown = set(ids) - {f["id"] for f in fixtures}
        if unknown:
            raise ValueError(f"Unknown fixture IDs: {sorted(unknown)}")
        fixtures = [f for f in fixtures if f["id"] in ids]
    extractor = None
    initialization_error = None
    try:
        extractor = engines.create(engine)
    except Exception as exc:  # noqa: BLE001 - third-party boundary, preserve ERROR evidence
        initialization_error = f"{type(exc).__name__}: {exc}"
    results = []
    for fixture in fixtures:
        raw, error = "", initialization_error
        if extractor is not None:
            try:
                raw = extractor.extract(DATA / "pdfs" / f"{fixture['id']}.pdf")
            except Exception as exc:  # noqa: BLE001 - third-party boundary
                error = f"{type(exc).__name__}: {exc}"
        result = evaluate(fixture, raw, mode=mode, error=error)
        result["pdf_sha256"] = digest(DATA / "pdfs" / f"{fixture['id']}.pdf")
        results.append(result)
    return envelope(results, engines.metadata(engine), command)


def write_json(path: Path, value: dict[str, Any]) -> None:
    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
