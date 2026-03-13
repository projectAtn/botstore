# BotStore Agent API (autonomous mode)

## 1) Search missing capabilities
`POST /agent/search-capabilities`

```json
{
  "user_id": "telegram:8258812165",
  "runtime": "openclaw",
  "intent": "book flight and notify calendar",
  "missing_capabilities": ["calendar.write", "message.send"],
  "limit": 5
}
```

## 2) Install by capability
`POST /agent/install-by-capability`

```json
{
  "user_id": "telegram:8258812165",
  "runtime": "openclaw",
  "required_capabilities": ["web.search", "calendar.write"]
}
```

## 3) Evaluate policy before autonomous install/use
`POST /agent/policy-evaluate`

```json
{
  "user_id": "telegram:8258812165",
  "runtime": "openclaw",
  "pack_id": 2
}
```

## 4) Submit outcome telemetry
`POST /agent/outcome`

```json
{
  "user_id": "telegram:8258812165",
  "task_id": "task_abc123",
  "runtime": "openclaw",
  "pack_id": 2,
  "success": true,
  "latency_ms": 1840
}
```

## 5) Query compatibility quickly
`GET /agent/compatibility/{pack_id}?runtime=openclaw&version=0.1.0`

---

Use these endpoints inside autonomous loops:
- detect gap → search → install → execute → report outcome.
