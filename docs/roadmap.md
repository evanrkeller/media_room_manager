# Roadmap (shadow build)

Feature-driven roadmap for our shadow build of Media Room Manager. Sequenced by user value, not architectural layer.

This is **our** roadmap — not the original author's. His sequence lives in `PLAN.md` and decomposes the work by architectural layer (data model → validators → persistence → inspection → profiles → adapters → resolver → orchestrator). Our sequence builds the same end product but reorders the work around real end-user outcomes, applying the build-half principle.

For the architectural baseline we are building toward, see [`README.md`](../README.md) and [`docs/adr/0001-adopt-readme-as-architectural-baseline.md`](adr/0001-adopt-readme-as-architectural-baseline.md).

## Sequencing principle

Each feature epic delivers a vertical slice of end-user-observable behavior. Each pulls in only the data model, persistence, plumbing, and docs that the slice actually requires. The next epic builds on what's already there and adds whatever the next user outcome needs. We never pre-build infrastructure for future epics.

When direction changes (and it will), there's less to throw away.

## Feature epics

### Epic 1 — User discovers what devices Media Room Manager supports

**Status:** in flight

**End-user outcome:** After installing the integration, a user can answer "what AV gear does this thing know about?" by querying HA. They see the bundled profile library before configuring anything of their own.

**Verification surface:** HA Developer Tools → WebSocket page → call `media_room_manager/list_profiles` and `media_room_manager/get_profile`.

**Pulls in (build-half):**

- Profile YAML schema (narrowed to fields these stories need)
- Profile loader for `custom_components/media_room_manager/profiles/bundled/`
- `ProfileRegistry` in-memory store
- 2 bundled starter profiles (Apple TV 4K + Marantz SR8015 — covers two categories)
- WebSocket commands: `list_profiles`, `get_profile`
- Docs: entries in `docs/websocket-api.md`; `docs/profile-schema.md` for the schema itself

**Deliberately deferred:** graph dataclass model for Device/Interface/Connection/Zone/etc., `SystemConfig` aggregate, `Store` persistence, validators for non-profile entities, `list_devices`/`list_zones`/`list_connections` commands, adapters, path resolver, orchestrator, panel. None of these are needed to deliver Epic 1.

### Epic 2 — User adds their first device to Media Room Manager (sketch)

**End-user outcome:** A user picks a profile from the library and binds it to one of their already-configured HA `media_player` entities. The integration creates a device record they can verify.

**Pulls in (sketch):** Device dataclass and validator, persistence (SystemConfig + Store) — narrowed to what Epic 2 needs, `register_device` / `list_devices` WebSocket commands, capability matching for entity binding.

### Epic 3 — Media Room Manager auto-suggests profiles for devices the user already has in HA (sketch)

**End-user outcome:** After install, the user opens HA's Repairs page and sees suggestions like "Found a Marantz SR8015 in your setup — confirm to add it to Media Room Manager." Confirming it adds the device.

**Pulls in (sketch):** discovery service (anchor matching + sibling matching, per `README.md` §14), HA repair flow integration, capability scoring.

### Beyond Epic 3

The remaining vision in `README.md` — zones, connections, virtual sources, adapters, path resolution, orchestration, the panel UI — is intentionally not roadmapped yet. Roadmap each epic only after the previous one ships, so we know what's actually required from the next slice.

## Decision log

When an epic surfaces a meaningful architectural decision, capture it as an ADR under `docs/adr/`. The roadmap stays product-shaped (epics + outcomes); the ADRs carry the architectural reasoning.
