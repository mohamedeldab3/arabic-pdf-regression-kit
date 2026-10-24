"""Deliberate synthetic mutations, not observed engine failures."""

import pytest

from arabic_pdf_regression.corpus import load_corpus, verify
from arabic_pdf_regression.evaluate import evaluate, exit_code, normalize, token_present


@pytest.mark.parametrize("fixture", load_corpus(), ids=lambda f: f["id"])
def test_positive_controls(fixture):
    result = evaluate(fixture, fixture["expected"], mode="strict")
    assert result["status"] == "PASS"
    assert all(result["checks"].values())


@pytest.mark.parametrize("mutation", [lambda s: s[::-1], lambda s: " ".join(s.split()[::-1])])
def test_reversal(mutation):
    fixture = load_corpus()[0]
    result = evaluate(fixture, mutation(fixture["expected"]))
    assert result["status"] == "FAIL"
    assert not result["checks"]["phrase_order"]
    assert result["differences"]


@pytest.mark.parametrize("index,key", [(2, "identifiers"), (4, "numbers"), (5, "numbers")])
@pytest.mark.parametrize("replacement", ["", "BROKEN"])
def test_tokens_and_correction(index, key, replacement):
    fixture = load_corpus()[index]
    mutated = fixture["expected"].replace(fixture[key][0], replacement)
    result = evaluate(fixture, mutated)
    assert not result["checks"][key]
    assert evaluate(fixture, fixture["expected"])["findings"] == []


def test_whitespace_modes():
    fixture = load_corpus()[0]
    raw = "  " + fixture["expected"].replace(" ", "  ").replace("\n", "\n\n")
    assert evaluate(fixture, raw, mode="strict")["status"] == "FAIL"
    result = evaluate(fixture, raw)
    assert result["status"] == "PASS"
    assert result["checks"]["strict"] is False
    assert normalize("ا\u0654", "nfc") == "أ"
    assert normalize("١٢٣،", "nfc-whitespace") == "١٢٣،"


def test_empty_error_skipped():
    fixture = load_corpus()[0]
    assert evaluate(fixture)["status"] == "FAIL"
    error = evaluate(fixture, error="Unavailable dependency")
    assert error["status"] == "ERROR"
    assert exit_code([error]) == 2
    assert exit_code([evaluate(fixture, skipped=True)]) == 2
    assert exit_code([]) == 2


def test_numeric_boundaries_and_paragraph_order():
    assert not token_present("123", "91234")
    assert not token_present("1250.75", "1250.750")
    assert not token_present("123", "123.45")
    assert token_present("١٢٣", "عدد ١٢٣،")
    fixture = load_corpus()[-1]
    assert not evaluate(fixture, "\n\n".join(fixture["pages"][::-1]))["checks"]["phrase_order"]


def test_corpus_checksums():
    assert verify() == []
