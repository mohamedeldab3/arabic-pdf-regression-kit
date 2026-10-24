# Changelog

## Unreleased

- Fix false-positive numeric-token checks around Arabic decimal/thousands separators.
- Reject inconsistent recorded-run summaries/exit codes and invalid engine metadata.
- Keep subset CI baselines consistent after selecting fixture rows.
- Add 19 internal-audit regression cases and documented before/after evidence.

## 0.1.0 - 2026-10-24

- Eight original Arabic/mixed-language text-layer fixtures with independent logical
  ground truth, provenance, licensed font, and visually reviewed PDF output.
- Strict/NFC/whitespace diagnostics, phrase ordering, exact identifiers/numbers,
  missing content, error handling, and positive/mutation controls.
- Optional Docling and pypdf extraction, raw JSON and escaped static HTML reports,
  per-check run comparisons, package installation and pinned CI integration.
- Real Docling extraction completed after recovering and verifying layout weights.
- Canonical LF corpus bytes fix checksum verification after a Linux checkout;
  installed-package verification preserves virtualenv interpreter symlink paths.
