from arabic_pdf_regression import runs


def test_initialization_failure_is_error(monkeypatch):
    def fail(_):
        raise ImportError("synthetic missing dependency")
    monkeypatch.setattr(runs.engines, "create", fail)
    result = runs.run("docling", "strict", ["arabic-only"], ["test"])
    assert result["summary"]["ERROR"] == 1
    assert result["exit_code"] == 2


def test_extraction_failure_is_error(monkeypatch):
    class Broken:
        def extract(self, path):
            raise RuntimeError("synthetic extraction failure")
    monkeypatch.setattr(runs.engines, "create", lambda _: Broken())
    result = runs.run("docling", "strict", ["arabic-only"], ["test"])
    assert result["results"][0]["status"] == "ERROR"
    assert "synthetic extraction failure" in result["results"][0]["findings"][0]["detail"]
