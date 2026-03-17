# Adapter E2E Demo (CopilotKitAdapter)

- Time: 2026-03-17T07:51:55.949195+00:00
- API: http://127.0.0.1:8787
- User: `telegram:botstore_demo:1001`
- Bound target: `openclaw-main/demo-agent`
- Top search result: `service-ops-verticals`

## Install response
```json
{
  "ok": true,
  "message": "Install pending approval #25",
  "action": "approval_pending",
  "data": {
    "approval_id": 25
  }
}
```

## Where response
```json
{
  "ok": true,
  "message": "Where packs are installed:\n- service-ops-verticals: activated \u2192 openclaw-main/demo-agent\n- service-ops-verticals: activated \u2192 openclaw-main/demo-agent",
  "action": "where",
  "data": {
    "count": 2
  }
}
```
