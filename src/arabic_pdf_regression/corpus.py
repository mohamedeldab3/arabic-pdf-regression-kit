"""Load, generate and verify the independently specified corpus."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DATA = Path(__file__).parent / "data"


def load_corpus(root: Path = DATA) -> list[dict[str, Any]]:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    fixtures = manifest["fixtures"]
    if not fixtures or len({f["id"] for f in fixtures}) != len(fixtures):
        raise ValueError("Corpus must contain unique fixture IDs")
    for fixture in fixtures:
        if not fixture["expected"] or not fixture["pages"]:
            raise ValueError("Empty ground truth")
        if fixture["expected"] != "\n\n".join(fixture["pages"]):
            raise ValueError("Ground truth differs from authored pages")
        for token in fixture["identifiers"] + fixture["numbers"] + fixture["phrases"]:
            if token not in fixture["expected"]:
                raise ValueError("Expectation absent from ground truth")
        if Path(fixture["id"]).name != fixture["id"] or "/" in fixture["id"]:
            raise ValueError("Unsafe fixture ID")
    return fixtures  # type: ignore[no-any-return]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate(destination: Path, root: Path = DATA) -> None:
    from fpdf import FPDF

    destination.mkdir(parents=True, exist_ok=True)
    for fixture in load_corpus(root):
        pdf = FPDF()
        pdf.set_creation_date(datetime(2026, 10, 24, tzinfo=UTC))
        pdf.set_title(fixture["id"])
        pdf.add_font("Noto", fname=str(root / "fonts/NotoNaskhArabic.ttf"))
        pdf.set_font("Noto", size=20)
        pdf.set_text_shaping(True, direction="rtl", language="ara")
        for page in fixture["pages"]:
            pdf.add_page()
            pdf.set_xy(20, 35)
            # Explicit LTR embeddings in render input only. Ground truth is logical
            # text without formatting controls; no extraction output is repaired.
            for token in fixture["identifiers"] + fixture["numbers"]:
                page = page.replace(token, "\u202a" + token + "\u202c")
            pdf.multi_cell(170, 14, page, align="R")
        pdf.output(str(destination / f"{fixture['id']}.pdf"))


def verify(root: Path = DATA) -> list[str]:
    failures = []
    for fixture in load_corpus(root):
        source = root / "sources" / f"{fixture['id']}.txt"
        if source.read_text(encoding="utf-8") != fixture["expected"]:
            failures.append(f"{fixture['id']}: source mismatch")
    hashes = json.loads((root / "sha256.json").read_text(encoding="utf-8"))
    for name, expected in hashes.items():
        path = root / name
        if not path.is_file() or digest(path) != expected:
            failures.append(f"{name}: checksum mismatch")
    required = {f"pdfs/{f['id']}.pdf" for f in load_corpus(root)}
    if not required.issubset(hashes):
        failures.append("Missing PDF checksums")
    return failures
