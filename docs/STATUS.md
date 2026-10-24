# v0.1 status

Completed: implementation plan, packaging, eight original PDFs, independent ground
truth/provenance/font license, visual inspection, deterministic evaluator, optional
real adapters, offline controls, CLI, comparison, portable escaped JSON/HTML,
CI configuration, contribution guide and version-pinned subset example.

Local delivery only: feature branch codex/arabic-pdf-regression-v01. No push,
package publication, deployment, application or upstream messages were performed.
Existing MIT license retained. No pre-existing implementation/uncommitted work.

Real pypdf evidence is recorded (8 FAIL, no extraction errors). All 35 offline
tests, lint, typing, build and the clean installed-wheel quickstart passed.
Docling 2.142.1 was installed and attempted: layout weights could not be fully
downloaded; explicit offline cache verification recorded 1 ERROR. See RESULTS.md
for the exact artifact/revision, observed attempts and reproduction commands.
No Docling Arabic accuracy result is claimed. Browser preview connection was also
unavailable; PDF visual QA and HTML unit/CLI checks completed independently.
Hosted CI has not run because these changes are local.

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
- [ ] Hosted CI execution and Linux/macOS verification.
- [ ] Complete Docling extraction after public layout model weights are available.
- [ ] Broader real-world corpus or demonstrated external adoption.
