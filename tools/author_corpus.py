"""Original authored ground truth; never derived from any extractor.

Run from repository root: python tools/author_corpus.py
Then: python -m arabic_pdf_regression.cli fixtures generate --output ...
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src/arabic_pdf_regression/data"
CASES = [
    ("arabic-only", ["arabic"], ["تشرق الشمس فوق المدينة\nيقرأ الطفل كتابا جديدا"], [], []),
    ("mixed-paragraph", ["arabic", "english", "bidi"],
     ["هذا تقرير عن Python ومكتبة Open Source في القاهرة"], ["Python", "Open Source"], []),
    ("invoice-id", ["identifier", "bidi"],
     ["رقم الفاتورة INV-2026-042 للعميل الجديد"], ["INV-2026-042"], []),
    ("product-order", ["identifier", "bidi"],
     ["تم شحن المنتج SKU-AB12 ضمن الطلب ORD-907"], ["SKU-AB12", "ORD-907"], []),
    ("two-digit-systems", ["digits", "arabic-indic"],
     ["عدد الكتب 123 وعدد الأقلام ١٢٣"], [], ["123", "١٢٣"]),
    ("amount-date", ["decimal", "date"],
     ["المبلغ 1250.75 جنيه بتاريخ 2026-10-24"], [], ["1250.75", "2026-10-24"]),
    ("paragraph-order", ["order", "paragraphs"],
     ["الفقرة الأولى بداية الرحلة\n\nالفقرة الثانية وصول القطار\n\nالفقرة الثالثة نهاية اليوم"], [], []),
    ("page-order", ["order", "pages"],
     ["الصفحة الأولى بدء العمل", "الصفحة الثانية مراجعة النتائج"], [], []),
]

fixtures = []
(ROOT / "sources").mkdir(parents=True, exist_ok=True)
for fixture_id, tags, pages, identifiers, numbers in CASES:
    expected = "\n\n".join(pages)
    (ROOT / "sources" / f"{fixture_id}.txt").write_text(expected, encoding="utf-8", newline="\n")
    fixtures.append({
        "id": fixture_id, "tags": tags, "pages": pages, "expected": expected,
        "phrases": [line for page in pages for line in page.splitlines() if line],
        "identifiers": identifiers, "numbers": numbers,
        "provenance": "Original synthetic content authored for this project; no issue attachments",
        "license": "MIT", "generation": "fpdf2 2.8.9 + uharfbuzz 0.57.0; fixtures generate",
    })
(ROOT / "manifest.json").write_text(
    json.dumps({"schema_version": 1, "fixtures": fixtures}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8", newline="\n",
)
