# ADR-0001: Adopt the original author's README as architectural baseline

**Status:** Accepted
**Date:** 2026-05-11
**Decision drivers:** Shadow build; head-to-head comparison; minimize spurious divergence

## Context

This fork (`evanrkeller/media_room_manager`) is a shadow build running in parallel with the original author's implementation. The purpose is to validate Keller Solutions' development philosophies (build-half, feature-driven epics, story-driven tickets, TDD) against the same target as the original author — not to design a different product.

The original author's `README.md` (76 KB, ~26 sections) constitutes a thorough technical specification: graph model, profile system, adapter mechanisms, path resolver, orchestrator, panel UX, storage layout, automation contracts, and explicit boundaries. `CLAUDE.md` adds coding standards, framework conventions, and load-bearing constraints (e.g., "no Python escape hatch in profile YAML," "WebSocket schema is a stable contract").

For the head-to-head comparison to be meaningful, we should build against the same target. Re-litigating the spec would either invent a different product, or generate noise that obscures what the methodology comparison is actually measuring.

## Decision

We adopt the original author's `README.md` and `CLAUDE.md` as our architectural baseline. All design decisions, terminology, data model shape, and stated boundaries described there apply to our build unless explicitly superseded by a later ADR in this directory.

## Consequences

- Our code targets the same data model, same five adapter mechanisms, same profile schema semantics, same WebSocket-contract discipline, same panel-as-only-UI principle, and same operational expectations the spec lays out.
- Future ADRs that diverge from the spec are explicit and reviewable — readers can scan `docs/adr/` for the points where we depart, rather than diffing entire docs.
- We are **not** locked into the original author's `PLAN.md` phase structure or `TASKS.md` task ordering. Those are his project-management artifacts, not part of the architectural spec. Our build-half, feature-driven approach reorganizes the work into feature epics that may sequence differently. This is the methodology under test — see `docs/roadmap.md`.
- If our implementation reveals a flaw in the spec (genuinely wrong, not just "we'd have done it differently"), we record an ADR explaining the issue and the resulting divergence. We do **not** silently rewrite the spec or his planning artifacts.

## Alternatives considered

- **Re-derive the design from scratch.** Rejected: produces a different product, breaks the head-to-head comparison's premise.
- **Adopt only the high-level vision; choose our own data model and protocols.** Rejected: same problem — too much spurious divergence to draw clean methodology conclusions.
- **Adopt the spec only as soft guidance and override at will.** Rejected: leaves "what's our baseline?" ambiguous in every session, drifting silently away from the comparison target.

## References

- Original author's `README.md` (architectural spec)
- Original author's `CLAUDE.md` (coding standards and boundaries)
- `CLAUDE.local.md` (our shadow-build context)
- `docs/roadmap.md` (our feature-driven epic sequence)
