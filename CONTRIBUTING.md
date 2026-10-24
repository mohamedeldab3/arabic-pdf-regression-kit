# Contributing a reproducer

Use Python 3.11+. Install `python -m pip install -e ".[dev,fixtures,pypdf]"`.
Keep default tests offline; do not require Docling weights or API credentials.

1. Author minimal original text in tools/author_corpus.py before any extraction.
   Include stable ID, tags, pages, ordered phrases, identifiers, numeric tokens.
   Never derive expected text from the engine under evaluation.
2. Provide provenance and explicit redistribution permission. No issue attachments
   or real personal/business documents without a suitable license and redaction.
3. Run author_corpus.py and regenerate PDFs with the pinned generator extras.
   Render every changed page; inspect Arabic joining, bidi runs, numbers and order.
4. Update data/sha256.json only after reviewing the intentional change. Hash every
   data file except the hash index itself. Preserve the font's OFL attribution.
5. Add positive controls and focused corruptions. Label synthetic mutations.
   Run pytest, ruff, mypy, build and clean installed-package verification.
6. Record exact engine version/config and raw output when reporting a real failure.
   ERROR is infrastructure failure, FAIL is a violated expectation, SKIPPED is not
   run. None may be represented as PASS. Do not imply upstream endorsement.

Reports preserve document text. Publish only authorized synthetic content and
inspect reports for local paths before sharing. HTML is escaped and has no scripts.
