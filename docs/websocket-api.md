# WebSocket API

Media Room Manager exposes a stable WebSocket command surface. The integration's panel and external automations consume this surface; this document is the contract.

Per the project's `CLAUDE.md` boundary, any change to this surface — adding, removing, or modifying a command — must update this document in the same commit as the code change.

## Commands

### `media_room_manager/list_profiles`

Return all device profiles known to the integration's bundled library.

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

## Stability

The WebSocket command surface is a stable contract. Renaming a command, removing a documented field, or changing a field's type is a breaking change. Adding new optional response fields is non-breaking.

Breaking changes require coordination with the integration's panel (when it lands) and any external consumers, plus an entry under a deprecation policy that's recorded as an ADR in `docs/adr/`.
