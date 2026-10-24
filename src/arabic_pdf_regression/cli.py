"""Small CLI: no models or optional engines imported by default."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .corpus import generate, load_corpus, verify
from .evaluate import MODES, evaluate
from .report import compare, render
from .runs import envelope, run, write_json


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("Expected JSON object")
    return value


def saved_outputs(value: dict[str, Any], mode: str, command: list[str]) -> dict[str, Any]:
    if value.get("schema_version") != 1 or not isinstance(value.get("outputs"), dict):
        raise ValueError("Expected schema_version=1 and outputs mapping")
    fixtures = load_corpus()
    unknown = set(value["outputs"]) - {f["id"] for f in fixtures}
    if unknown:
        raise ValueError(f"Unknown fixture IDs: {sorted(unknown)}")
    results = []
    for fixture in fixtures:
        item = value["outputs"].get(fixture["id"])
        if item is None:
            result = evaluate(fixture, mode=mode, skipped=True)
        elif not isinstance(item, dict) or not isinstance(item.get("raw", ""), str):
            raise ValueError("Each output must be an object with string raw text")
        else:
            error = item.get("error")
            if error is not None and (not isinstance(error, str) or not error):
                raise ValueError("error must be a non-empty string")
            result = evaluate(fixture, item.get("raw", ""), mode=mode, error=error)
        results.append(result)
    engine = value.get("engine", {"name": "saved-output", "version": None})
    return envelope(results, engine, command)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Independent Arabic PDF regression diagnostics")
    sub = parser.add_subparsers(dest="command", required=True)
    fixtures = sub.add_parser("fixtures")
    fixture_sub = fixtures.add_subparsers(dest="action", required=True)
    fixture_sub.add_parser("verify")
    fixture_sub.add_parser("generate").add_argument("--output", type=Path, required=True)
    for name in ("run", "evaluate"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--output", type=Path, required=True)
        cmd.add_argument("--html", type=Path)
        cmd.add_argument("--mode", choices=MODES, default="nfc-whitespace")
        if name == "run":
            cmd.add_argument("--engine", choices=("docling", "pypdf"), required=True)
            cmd.add_argument("--ids", nargs="+")
        else:
            cmd.add_argument("input", type=Path)
    report = sub.add_parser("report")
    report.add_argument("input", type=Path)
    report.add_argument("--html", type=Path, required=True)
    diff = sub.add_parser("compare")
    diff.add_argument("before", type=Path)
    diff.add_argument("after", type=Path)
    diff.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    command = ["arabic-pdf-kit", *(sys.argv[1:] if argv is None else argv)]
    try:
        if args.command == "fixtures":
            if args.action == "generate":
                generate(args.output)
                print(f"Generated {len(load_corpus())} PDFs")
                return 0
            failures = verify()
            print(json.dumps({"verified": not failures, "findings": failures}))
            return 2 if failures else 0
        if args.command == "compare":
            value = compare(read_json(args.before), read_json(args.after))
            write_json(args.output, value)
            print(json.dumps({k: len(value[k]) for k in ("regressions", "improvements", "incomparable")}))
            return int(value["exit_code"])
        if args.command == "report":
            value = read_json(args.input)
        else:
            if args.command == "run":
                failures = verify()
                if failures:
                    raise ValueError("Packaged corpus integrity check failed")
                value = run(args.engine, args.mode, args.ids, command)
            else:
                value = saved_outputs(read_json(args.input), args.mode, command)
            write_json(args.output, value)
            print(json.dumps(value["summary"]))
        if args.html:
            args.html.parent.mkdir(parents=True, exist_ok=True)
            args.html.write_text(render(value), encoding="utf-8")
        return 0 if args.command == "report" else int(value["exit_code"])
    except (OSError, ValueError, KeyError, TypeError) as exc:
        # Do not print document contents or malformed JSON text to logs.
        print(f"Input/report error ({type(exc).__name__}); check paths and schema", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
