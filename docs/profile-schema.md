# Profile YAML schema

This document is the contract for the YAML profile format that ships in `custom_components/media_room_manager/profiles/bundled/`. Per `CLAUDE.md`, any change to the schema in `custom_components/media_room_manager/profiles/schema.py` must update this document and the example bundled profiles in the same commit.

The schema is **permissive at the top level** (`extra=ALLOW_EXTRA`) — bundled or community profiles may include fields the dataclass does not yet surface, and later stories extend the dataclass to start surfacing those fields without breaking existing YAMLs.

## Required top-level fields

| Field | Type | Description |
|---|---|---|
| `profile_id` | string | Stable identifier; convention is `manufacturer_model_kebab` (e.g., `apple_tv_4k`). |
| `manufacturer` | string | Device manufacturer (e.g., `Apple`, `Marantz`). |
| `model` | string | Device model (e.g., `TV 4K`, `SR8015`). |
| `category` | string | Free-form device category for grouping (e.g., `streamer`, `avr`, `processor`, `display`, `matrix`, `splitter`, `audio_extractor`). Not yet enum-validated — tightens when a story needs categorical filtering. |
| `power_handling` | enum | One of `discrete_capable`, `toggle`, `always_on`, `disabled`. The set is fixed at the spec level (`CLAUDE.md`) and intentionally not extensible. |

## Optional top-level fields

| Field | Type | Default | Description |
|---|---|---|---|
| `power_on_delay` | integer | `0` | Seconds the orchestrator should wait after sending power-on before issuing further commands. |
| `output_groups` | list of objects | `[]` | Device-internal output groups (see below). |
| `interfaces` | list of objects | `[]` | Physical input/output ports (see below). |
| `virtual_sources` | list of objects | `[]` | Static virtual sources intrinsic to the device (e.g., an AVR's tuner). |

## Structural fields — current contract

The structural lists (`output_groups`, `interfaces`, `virtual_sources`) accept lists of arbitrary dicts. The schema does **not** currently enforce required keys inside these dicts — that intentionality holds until a story actually needs to act on the structures (e.g., path resolution).

The bundled starter profiles use a consistent shape that future tightening will likely codify:

### `output_groups[]` — typical fields

| Field | Type | Notes |
|---|---|---|
| `id` | string | Stable id within the profile (e.g., `main`, `zone2`, `hdmi_out`). |

### `interfaces[]` — typical fields

| Field | Type | Notes |
|---|---|---|
| `id` | string | Stable id within the profile (e.g., `hdmi_1`). |
| `direction` | string | `input` or `output`. |
| `type` | string | Carrier type (e.g., `hdmi`, `optical`, `coax`, `analog_audio`). |
| `label` | string | Human-readable label as printed on the chassis. |
| `output_group` | string | Required for outputs — the `output_groups[].id` this output belongs to. |
| `routable_to_output_group` | list of strings | Required for inputs — the `output_groups[].id`s this input can route to. |

### `virtual_sources[]` — typical fields

| Field | Type | Notes |
|---|---|---|
| `id` | string | Stable id within the profile (e.g., `tuner`). |
| `label` | string | Human-readable label (e.g., `AM/FM Tuner`). |
| `routable_to_output_group` | string | The `output_groups[].id` this virtual source feeds. |

## Top-level fields not yet validated

The original author's `README.md` describes additional fields we have not yet introduced into the schema — `schema_version`, `exclusive_outputs`, `inputs_are_exclusive_per_output_group`, `aux_entities`, `dynamic_virtual_sources`, `discovery`. These are accepted today via `extra=ALLOW_EXTRA` and will be surfaced into the dataclass + validated as later stories require them.

## Example: minimum valid profile

```yaml
profile_id: apple_tv_4k
manufacturer: Apple
model: TV 4K
category: streamer
power_handling: discrete_capable
```

## Example: profile with structural fields

```yaml
profile_id: marantz_sr8015
manufacturer: Marantz
model: SR8015
category: avr
power_handling: discrete_capable
power_on_delay: 0
output_groups:
  - id: main
interfaces:
  - id: hdmi_1
    direction: input
    type: hdmi
    label: HDMI 1
    routable_to_output_group: [main]
  - id: hdmi_out_main
    direction: output
    type: hdmi
    label: HDMI Out (Main)
    output_group: main
virtual_sources:
  - id: tuner
    label: AM/FM Tuner
    routable_to_output_group: main
```

## Stability

Adding new optional top-level fields is non-breaking. Removing required fields, changing a field's type, or shrinking the `power_handling` allowed set is breaking and requires an ADR in `docs/adr/` documenting the migration plan.
