# Architecture Decision Records

This directory holds Architecture Decision Records (ADRs) for our shadow build of Media Room Manager. ADRs capture the **why** behind specific architectural choices and document trade-offs so future contributors (and future-us) understand the reasoning behind the code.

## When to write an ADR

Write an ADR when:

- You make a non-trivial architectural choice (data model shape, framework, validation library, protocol, persistence strategy).
- You explicitly adopt or reject a decision present in the original author's `README.md`.
- You diverge from the spec in a way that future readers should understand.
- You make a decision that would surprise a reader who only looked at the code.

Do **not** write an ADR for:

- Routine implementation choices (variable naming, file structure within a module, library version bumps).
- Decisions already obviously communicated by the code or by the original spec.
- Decisions the original author already records in `README.md` and we're inheriting without modification (one umbrella ADR covers spec adoption — see ADR-0001).

## How ADRs relate to other docs

- **`README.md`** (the original author's spec) — the forward-looking design we are building toward.
- **`docs/adr/`** (this directory) — discrete decisions, with context and trade-offs, that shape how we implement that design.
- **`docs/roadmap.md`** — feature ordering for our shadow build.
- **GitHub Issues** — the **what** we're building (stories from the end user's perspective).

Together: stories say *what* we're delivering; ADRs and `README.md` cover *why* and *how* the architecture supports that delivery.

## File naming

`NNNN-<short-kebab-title>.md` where NNNN is a zero-padded sequence number. Examples:

- `0001-adopt-readme-as-architectural-baseline.md`
- `0002-voluptuous-for-schema-validation.md`
- `0017-replace-mrmstore-with-sqlite-backed-store.md` (hypothetical divergence)

ADR numbers are never reused. A superseded ADR keeps its number; the superseding ADR cites it.

## Template

```markdown
# ADR-NNNN: <title>

**Status:** Proposed | Accepted | Superseded by ADR-NNNN
**Date:** YYYY-MM-DD
**Decision drivers:** <short list — what forced this decision>

## Context

What's the situation? What constraints apply? What's already decided elsewhere (cite README sections or other ADRs)?

## Decision

The single, concrete decision in one or two sentences. Active voice.

## Consequences

What does choosing this entail? What does it rule out? What downstream work does it enable or block?

## Alternatives considered

List the options that were on the table and why each was rejected. Brief — one or two sentences each.

## References

- Citations to `README.md` sections, external docs, prior ADRs, or commits.
```

Keep ADRs short. A good ADR fits on one screen. If you need more than a screen, the decision is probably actually several decisions that should each have their own ADR.

## Status lifecycle

- **Proposed** — under discussion; the decision hasn't been adopted yet.
- **Accepted** — the decision is in force and code may rely on it.
- **Superseded** — a later ADR replaces this one. The ADR stays in the directory for history; its Status line points to the superseding ADR.
