# v0.1 status

Completed: implementation plan, packaging, eight original PDFs, independent ground
truth/provenance/font license, visual inspection, deterministic evaluator, optional
real adapters, offline controls, CLI, comparison, portable escaped JSON/HTML,
CI configuration, contribution guide and version-pinned subset example.

Work was implemented on codex/arabic-pdf-regression-v01 and pushed after explicit
user authorization. The verified implementation is being delivered on main.
No package publication, deployment, application submission or upstream messages
were performed.
Existing MIT license retained. No pre-existing implementation/uncommitted work.

Real pypdf evidence is recorded (8 FAIL, no extraction errors). All 35 offline
tests at the initial release passed. The internal maintenance audit expanded the
suite to 54 passing tests and fixed numeric boundaries and run-metadata consistency;
see MAINTENANCE_LOG.md. Lint, typing, build and installed-wheel checks are included
in verification.
Docling 2.142.1 completed all eight fixtures: 0 PASS, 8 FAIL, 0 ERROR, 0 SKIPPED.
The layout-model download was recovered and SHA-256 verified. pypdf 6.21.1 and
6.21.2 were both measured; their per-check comparison found no changes.
See RESULTS.md for artifacts/revisions and reproduction commands. Browser preview was
unavailable; PDF visual QA and HTML unit/CLI checks completed independently.
Hosted CI passed Windows/Linux x Python 3.11/3.12 at commit 1dae18f; see RESULTS.md.
The application packet and six-month maintenance plan are prepared in docs/.

To continue: read RESULTS.md first, reproduce the installed-wheel quickstart, then
prioritize additional engine-version evidence and authorized real-world cases.
Do not expand into scanned OCR before the current text-layer evidence is understood.
No upstream issue may be described as a confirmed current defect without reproducing
that specific document/configuration.

Public demonstration checklist:
- [x] Original licensed fixtures, sources, explicit contracts and font attribution.
- [x] Real raw extraction evidence separated from synthetic mutation controls.
- [x] CLI diagnostics and shareable static report with version/config/repro command.
- [x] Test, typing, lint, packaging and clean-install verification tooling.
- [x] Honest early-stage description and explicit limits.
- [x] Hosted CI execution and Linux/Windows verification.
- [x] Complete Docling extraction after public layout model weights are available.
- [x] Prepared application answers under the official 500-character limits.
- [ ] macOS verification.
- [ ] Broader real-world corpus or demonstrated external adoption.
