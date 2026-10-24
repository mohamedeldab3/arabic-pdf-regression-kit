# Roadmap

## Shipped in v0.1
- Eight original text-layer fixtures and nine visually inspected pages.
- Explicit strict/NFC/whitespace diagnostics and token/order checks.
- Optional Docling and pypdf adapters, saved outputs, JSON/HTML and run comparison.
- Offline mutation/positive controls, packaging and CI configuration.

## Next evidence and usability work
- Reproduce across Linux/macOS and multiple pinned engine versions.
- Add structured run-schema validation and richer missing-content diagnostics.
- Add an authorized real-world reproducer when one is available.
- Audit deterministic PDF byte reproduction across pinned fonttools versions.

## Future scope, not shipped
- Scanned PDFs, OCR language/configuration matrices and model cache management.
- Columns, tables, diacritics, ligatures, longer documents and page-local findings.
- Statistical accuracy evaluation and a broader licensed corpus.

No SaaS, custom OCR training or upstream adoption claims are planned for v0.1.
