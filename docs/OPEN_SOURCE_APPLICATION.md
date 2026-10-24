# Codex for Open Source application packet

Prepared against the official pages reviewed on 2026-10-24:
- [Program](https://developers.openai.com/community/codex-for-oss)
- [Application form](https://openai.com/form/codex-for-oss/)
- [Program terms](https://learn.chatgpt.com/docs/codex-for-oss-terms)

This is a prepared application, not a submission or an acceptance claim. Selection
is OpenAI's decision. The useful evidence here is original licensed fixtures,
reproducible measurements, verified tooling, and a concrete maintenance purpose.
No external adoption, usage volume, endorsements, or upstream maintainer role is
claimed. Refresh public links and CI status immediately before submitting.

## Form fields

GitHub username: `mohamedeldab3`

Repository: https://github.com/mohamedeldab3/arabic-pdf-regression-kit

Role: **Primary maintainer**, subject to your confirmation that this describes
your actual repository responsibilities. This role is for this kit, not Docling.

Enter your own first/last name and the email associated with your ChatGPT account
in the form. These personal account details are not stored in the public repo.

### Why does this repository qualify? (under 500 characters)

I maintain an MIT-licensed regression kit for Arabic PDF extraction. Original text-layer fixtures, explicit word-order/identifier/number checks, raw Docling and pypdf runs, version comparisons, and portable reports make failures reproducible for document-processing and RAG maintainers. Its ecosystem value is targeted Arabic diagnostics and repeatable upgrade checks; I am not claiming measured external adoption.

### Anything else we should know? (under 500 characters)

I maintain fixture specifications and provenance, evaluator correctness, engine adapters, packaging, documentation, and CI. I would use ChatGPT Pro with Codex for regression triage, code review, cross-version testing, and contributor support. The repository includes positive controls, deliberate mutation tests, recorded real-engine outputs, and reproducible installation instructions. FAIL results remain visible; infrastructure errors are never counted as passes.

### Optional API-credit answer (only if you request that separate benefit)

I would use credits for maintainer-assisted issue triage, review of proposed fixture additions, and release-note drafting from recorded compatibility changes. Deterministic evaluation and engine baselines would remain offline and independently verifiable; model-generated suggestions would never be ground truth or substitute for real extraction evidence.

API credits and Codex Security are optional interests. The kit's core needs
neither a paid API nor an API key. Supply your actual Organization ID only in the
official form if requested; do not commit account identifiers or credentials.

## Evidence to attach or link

- [README and quickstart](../README.md)
- [Measured results and limitations](RESULTS.md)
- [Docling raw run](../evidence/docling-2.142.1.json)
- [pypdf raw run](../evidence/pypdf.json)
- [Corpus/source/font provenance](CORPUS.md)
- [Pinned subset CI example](../examples/ci-subset.yml)
- [Public CI runs](https://github.com/mohamedeldab3/arabic-pdf-regression-kit/actions)
- [Maintenance history](https://github.com/mohamedeldab3/arabic-pdf-regression-kit/commits/main/)
- [Six-month maintenance plan](MAINTENANCE_PLAN.md)
- [Reproduced internal findings and fixes](MAINTENANCE_LOG.md)

## Before submitting

- Confirm repository and GitHub profile are publicly visible.
- Open the default-branch README and verify the linked artifacts exist.
- Check CI for the exact submitted commit; do not describe pending jobs as passed.
- Confirm primary-maintainer responsibility and repository write access.
- Review the official terms and complete identity/account fields yourself.
- Describe supported maintenance work and measured results without inventing users,
  downloads, PR reviews, issue activity, endorsements, or promises of acceptance.

Implementation completion is not itself evidence of meaningful usage or sustained
maintenance. Those remain separate signals for the program's review.
