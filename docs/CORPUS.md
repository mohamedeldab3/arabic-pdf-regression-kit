# Corpus provenance and generation

All eight text sources are original synthetic examples, MIT licensed under LICENSE.
`tools/author_corpus.py` is the authoring source; manifest.json and sources/*.txt
are independent expected logical text, never extracted from generated PDFs.

Noto Naskh Arabic variable font: Google/Noto authors, SIL Open Font License 1.1,
bundled unchanged with its OFL.txt. Downloaded 2026-10-24 from
https://github.com/google/fonts/tree/main/ofl/notonaskharabic .
Exact downloaded bytes are identified by data/sha256.json. Font is embedded in PDFs.
MIT applies to our content/code, not to the font, whose OFL remains applicable.

Generator: fpdf2 2.8.9 with uharfbuzz 0.57.0. HarfBuzz shapes glyphs and fpdf2
handles bidirectional runs; no manual reversal. Deterministic creation timestamp.
Expected identifiers/numbers receive Unicode LTR embeddings in rendering input
only, so the ISO date displays as 2026-10-24. Logical ground truth has no bidi
formatting controls. The evaluator does not remove controls from extracted text.
`arabic-pdf-kit fixtures generate --output regenerated` regenerates PDFs from
the packaged manifest. `fixtures verify` verifies the committed corpus against
hashes and independent source text. PDF byte stability is only expected with
the pinned generator stack, including the fonttools version recorded in results.

Each phrase is an exact line, searched in increasing logical offset. Page-order
case expects first-page text before second-page text. These tests do not validate
arbitrary tables, columns, handwriting, ligature fidelity or scanned OCR.
