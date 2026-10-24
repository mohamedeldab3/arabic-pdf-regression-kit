"""Internal audit reproductions, not reports attributed to external users."""

import copy
import json

import pytest

from arabic_pdf_regression.cli import main, saved_outputs
from arabic_pdf_regression.corpus import load_corpus
from arabic_pdf_regression.evaluate import evaluate, token_present
from arabic_pdf_regression.report import compare, render


def positive_run():
    return saved_outputs({
        "schema_version": 1,
        "outputs": {f["id"]: {"raw": f["expected"]} for f in load_corpus()},
    }, "strict", ["internal-audit"])


@pytest.mark.parametrize("token,raw", [
    ("123", "٩٬123"), ("١٢٣", "١٢٣٫٤"), ("1250.75", "1250.75٫9"),
    ("123", "123٬٤٥٦"), ("123", "٩٫123"), ("١٢٣", "٤٬١٢٣"),
])
def test_arabic_numeric_separator_does_not_hide_a_changed_number(token, raw):
    assert not token_present(token, raw)


def test_numeric_finding_is_removed_by_actual_correction():
    fixture = next(f for f in load_corpus() if f["id"] == "two-digit-systems")
    corrupted = fixture["expected"].replace("123", "٩٬123")
    result = evaluate(fixture, corrupted)
    assert result["checks"]["numbers"] is False
    assert result["raw"] == corrupted
    assert evaluate(fixture, fixture["expected"])["checks"]["numbers"] is True
    assert token_present("١٢٣", "عدد ١٢٣،")


@pytest.mark.parametrize("mutation", [
    {"summary": {"PASS": 0, "FAIL": 0, "ERROR": 0, "SKIPPED": 0}},
    {"summary": {"PASS": 8}},
    {"summary": {"PASS": True, "FAIL": 0, "ERROR": 0, "SKIPPED": 0}},
    {"exit_code": 1}, {"exit_code": False}, {"schema_version": True},
])
def test_inconsistent_recorded_metadata_is_rejected(mutation, tmp_path):
    original = positive_run()
    corrupted = copy.deepcopy(original)
    corrupted.update(mutation)
    with pytest.raises(ValueError):
        render(corrupted)
    with pytest.raises(ValueError):
        compare(original, corrupted)
    path = tmp_path / "corrupted.json"
    destination = tmp_path / "report.html"
    path.write_text(json.dumps(corrupted), encoding="utf-8")
    assert main(["report", str(path), "--html", str(destination)]) == 2
    assert not destination.exists()
    assert "<html" in render(original)


@pytest.mark.parametrize("engine", [None, "pypdf", {}, {"name": 5},
                                    {"name": "", "version": "1"},
                                    {"name": "pypdf", "version": 5}])
def test_invalid_saved_engine_is_rejected_before_writing_artifacts(engine, tmp_path):
    source = tmp_path / "input.json"
    output = tmp_path / "run.json"
    source.write_text(json.dumps({"schema_version": 1, "engine": engine, "outputs": {}}), encoding="utf-8")
    assert main(["evaluate", str(source), "--output", str(output)]) == 2
    assert not output.exists()
