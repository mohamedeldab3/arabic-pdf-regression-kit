# Related work (reviewed 2026-10-24)

[arabic-ocr-bench](https://github.com/Antonhansel/arabic-ocr-bench) provides broader
multi-engine/model evaluation, real scans and per-page scores. This kit instead
ships eight tiny original text-layer cases with explicit identifier/numeric/order
contracts and compatible-run comparisons. These scopes are complementary; we do
not claim novelty across every feature or superiority in extraction accuracy.

[Docling #1938](https://github.com/docling-project/docling/issues/1938): a human
reported reversed Arabic. A human maintainer closed it on 2026-10-14 after no
reply, asking for a current version and reproducer. Its bot explanation is not
evidence of the present implementation. We do not redistribute its attachments.

[Docling #3021](https://github.com/docling-project/docling/issues/3021) is an open
scanned Arabic OCR question. Its author disputes bot configuration suggestions.
The [current OCR docs](https://docling-project.github.io/docling/concepts/OCR/)
describe language and engine options; historical bot advice must not replace them.
Our OCR-disabled cases cannot establish anything about scanned OCR performance.

The adapter follows Docling's [DocumentConverter reference](https://docling-project.github.io/docling/reference/document_converter/)
and [PdfPipelineOptions reference](https://docling-project.github.io/docling/reference/pipeline_options/).
Even with OCR/table structure disabled, the standard pipeline may download layout
weights. Model/network failures are ERROR, not failed Arabic expectations.

Generation follows [fpdf2 text shaping](https://py-pdf.github.io/fpdf2/TextShaping.html).
None of the referenced maintainers has adopted, requested or endorsed this kit
based on evidence available to this project.
