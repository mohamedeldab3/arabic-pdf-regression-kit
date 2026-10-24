"""Optional real extractors. No extractor imports occur during unit tests."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Protocol


class Extractor(Protocol):
    def extract(self, path: Path) -> str: ...


class PypdfExtractor:
    def extract(self, path: Path) -> str:
        from pypdf import PdfReader

        return "\n\n".join(page.extract_text() or "" for page in PdfReader(path).pages)


class DoclingExtractor:
    def __init__(self) -> None:
        from docling.datamodel.accelerator_options import (
            AcceleratorDevice,
            AcceleratorOptions,
        )
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.document_converter import DocumentConverter, PdfFormatOption

        options = PdfPipelineOptions(do_ocr=False, do_table_structure=False)
        options.accelerator_options = AcceleratorOptions(device=AcceleratorDevice.CPU)
        self.converter = DocumentConverter(format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=options),
        })

    def extract(self, path: Path) -> str:
        from docling.datamodel.base_models import ConversionStatus

        result = self.converter.convert(path)
        if result.status != ConversionStatus.SUCCESS:
            raise RuntimeError(f"Docling conversion status: {result.status}")
        return str(result.document.export_to_text())


def metadata(engine: str) -> dict[str, Any]:
    try:
        installed = version(engine)
    except PackageNotFoundError:
        installed = None
    return {"name": engine, "version": installed,
            "configuration": {"ocr": False, "device": "cpu", "table_structure": False}
            if engine == "docling" else {"extraction_mode": "plain", "ocr": False}}


def create(engine: str) -> Extractor:
    if engine == "pypdf":
        return PypdfExtractor()
    if engine == "docling":
        return DoclingExtractor()
    raise ValueError(f"Unknown engine: {engine}")
