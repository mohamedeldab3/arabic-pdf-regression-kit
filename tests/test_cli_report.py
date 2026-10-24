import copy
import json

import pytest

from arabic_pdf_regression.cli import main, saved_outputs
from arabic_pdf_regression.corpus import load_corpus
from arabic_pdf_regression.report import compare, render


def control():
    return {"schema_version": 1, "engine": {"name": "synthetic-control", "version": "1"},
            "outputs": {f["id"]: {"raw": f["expected"]} for f in load_corpus()}}


def test_cli_saved_roundtrip_and_report(tmp_path, capsys):
    source, output, html = (tmp_path / name for name in ("source.json", "run.json", "run.html"))
    source.write_text(json.dumps(control()), encoding="utf-8")
    assert main(["evaluate", str(source), "--output", str(output), "--html", str(html)]) == 0
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["summary"]["PASS"] == 8
    assert main(["report", str(output), "--html", str(html)]) == 0
    assert "<html" in html.read_text(encoding="utf-8")
    assert "تشرق" not in capsys.readouterr().out
    assert main(["fixtures", "verify"]) == 0


def test_missing_output_is_skipped_and_error_is_not_pass():
    value = control()
    del value["outputs"]["arabic-only"]
    value["outputs"]["invoice-id"] = {"error": "synthetic engine error"}
    result = saved_outputs(value, "strict", ["test"])
    assert result["summary"]["SKIPPED"] == 1
    assert result["summary"]["ERROR"] == 1
    assert result["exit_code"] == 2


def test_compare_both_directions_and_within_failures(tmp_path):
    good = saved_outputs(control(), "strict", ["test"])
    corrupted = control()
    corrupted["outputs"]["invoice-id"]["raw"] = "رقم الفاتورة WRONG"
    bad = saved_outputs(corrupted, "strict", ["test"])
    assert compare(good, bad)["regressions"]
    assert compare(bad, good)["improvements"]
    assert compare(good, good)["exit_code"] == 0
    partial = copy.deepcopy(bad)
    partial["results"][2]["checks"]["identifiers"] = True
    assert compare(bad, partial)["improvements"] == [{"id": "invoice-id", "check": "identifiers"}]
    a, b, dest = (tmp_path / name for name in ("a.json", "b.json", "diff.json"))
    a.write_text(json.dumps(good), encoding="utf-8")
    b.write_text(json.dumps(bad), encoding="utf-8")
    assert main(["compare", str(a), str(b), "--output", str(dest)]) == 1


def test_incomparable_errors_modes_and_removed_fixtures():
    good = saved_outputs(control(), "strict", ["test"])
    changed = copy.deepcopy(good)
    changed["results"][0]["status"] = "ERROR"
    assert compare(good, changed)["exit_code"] == 2
    changed["results"].pop(0)
    assert compare(good, changed)["exit_code"] == 2
    changed = copy.deepcopy(good)
    changed["results"][0]["mode"] = "nfc"
    with pytest.raises(ValueError):
        compare(good, changed)


def test_html_escapes_every_untrusted_surface():
    run = saved_outputs(control(), "strict", ["<script>alert(1)</script>"])
    row = run["results"][0]
    payload = '<img src=x onerror="alert(1)">'
    row["raw"] = payload
    row["id"] = payload
    row["expectations"]["expected"] = payload
    row["findings"] = [{"detail": payload}]
    html = render(run)
    assert "<script>" not in html and "<img " not in html
    assert "&lt;img" in html and "&lt;script&gt;" in html


def test_raw_controls_are_visible_without_modifying_saved_text():
    value = control()
    value["outputs"]["arabic-only"]["raw"] = "نص\x06\r\n "
    run = saved_outputs(value, "strict", ["test"])
    html = render(run)
    assert run["results"][0]["raw"] == "نص\x06\r\n "
    assert "\\u0006\\r\\n " in html
    assert "\x06" not in html


@pytest.mark.parametrize("value", [[], {"schema_version": 9}, {"schema_version": 1, "outputs": {"unknown": {}}}])
def test_bad_input_exits_two(tmp_path, value):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    assert main(["evaluate", str(path), "--output", str(tmp_path / "out.json")]) == 2


def test_unknown_fixture_ids_are_errors(tmp_path):
    assert main(["run", "--engine", "pypdf", "--ids", "unknown", "--output", str(tmp_path / "r.json")]) == 2


@pytest.mark.parametrize("changes", [{"results": []}, {"results": [42]}, {"schema_version": 2}])
def test_invalid_recorded_run_is_input_error(tmp_path, changes):
    value = saved_outputs(control(), "strict", ["test"])
    value.update(changes)
    path = tmp_path / "bad-run.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    assert main(["report", str(path), "--html", str(tmp_path / "out.html")]) == 2
