# WebSocket API

Media Room Manager exposes a stable WebSocket command surface. The integration's panel and external automations consume this surface; this document is the contract.

Per the project's `CLAUDE.md` boundary, any change to this surface — adding, removing, or modifying a command — must update this document in the same commit as the code change.

## Commands

### `media_room_manager/list_profiles`

Return all device profiles known to the integration's bundled library — identity fields only. For the full structural detail of a single profile, use [`get_profile`](#media_room_managerget_profile).

**Parameters:** none.

**Response:** a JSON array of profile entries. Each entry is an object containing at minimum:

| Field | Type | Description |
|---|---|---|
| `profile_id` | string | Stable identifier for the profile (e.g., `apple_tv_4k`). |
| `manufacturer` | string | Device manufacturer (e.g., `Apple`). |
| `model` | string | Device model (e.g., `TV 4K`). |
| `category` | string | Device category (e.g., `streamer`, `avr`). |

If no profiles are bundled, the response is an empty array `[]` (never an error).

**Example request:**

```json
{
  "id": 7,
  "type": "media_room_manager/list_profiles"
}
```

**Example response:**

```json
{
  "id": 7,
  "type": "result",
  "success": true,
  "result": [
    {
      "profile_id": "apple_tv_4k",
      "manufacturer": "Apple",
      "model": "TV 4K",
      "category": "streamer"
    },
    {
      "profile_id": "marantz_sr8015",
      "manufacturer": "Marantz",
      "model": "SR8015",
      "category": "avr"
    }
  ]
}
```

**Added in:** v0.0.1 (story #45).

---

### `media_room_manager/get_profile`

Return the full profile for a given `profile_id`, including identity fields and structural fields (output groups, interfaces, virtual sources, power handling).

**Parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| `profile_id` | string | yes | The id of the profile to retrieve. |

**Response (success):** an object containing identity and structural fields.

| Field | Type | Description |
|---|---|---|
| `profile_id` | string | Stable identifier for the profile. |
| `manufacturer` | string | Device manufacturer. |
| `model` | string | Device model. |
| `category` | string | Device category. |
| `power_handling` | string | One of `discrete_capable`, `toggle`, `always_on`, `disabled`. See `CLAUDE.md`. |
| `power_on_delay` | integer | Seconds the orchestrator should wait after sending power-on before issuing further commands. Defaults to `0`. |
| `output_groups` | array of objects | Device-internal output groups. Each entry has at minimum an `id`. Inner shape is loose at this stage; later commands may surface a tighter contract. |
| `interfaces` | array of objects | Physical input/output interfaces. Outputs declare `output_group`; inputs declare `routable_to_output_group`. |
| `virtual_sources` | array of objects | Static virtual sources declared by the profile (e.g., an AVR's tuner). |

**Response (error — unknown profile):**

| Field | Value |
|---|---|
| `success` | `false` |
| `error.code` | `not_found` |
| `error.message` | Names the unknown `profile_id`. |

**Response (error — missing or wrong-type `profile_id`):**

| Field | Value |
|---|---|
| `success` | `false` |
| `error.code` | `invalid_format` |
| `error.message` | HA-supplied schema-validation message. |

**Example request:**

```json
{
  "id": 8,
  "type": "media_room_manager/get_profile",
  "profile_id": "apple_tv_4k"
}
```

**Example response:**

```json
{
  "id": 8,
  "type": "result",
  "success": true,
  "result": {
    "profile_id": "apple_tv_4k",
    "manufacturer": "Apple",
    "model": "TV 4K",
    "category": "streamer",
    "power_handling": "discrete_capable",
    "power_on_delay": 0,
    "output_groups": [
      {"id": "hdmi_out"}
    ],
    "interfaces": [
      {
        "id": "hdmi",
        "direction": "output",
        "type": "hdmi",
        "label": "HDMI",
        "output_group": "hdmi_out"
      }
    ],
    "virtual_sources": []
  }
}
```

**Added in:** v0.0.2 (story #46).

---

## Stability

The WebSocket command surface is a stable contract. Renaming a command, removing a documented field, or changing a field's type is a breaking change. Adding new optional response fields is non-breaking.

Breaking changes require coordination with the integration's panel (when it lands) and any external consumers, plus an entry under a deprecation policy that's recorded as an ADR in `docs/adr/`.
