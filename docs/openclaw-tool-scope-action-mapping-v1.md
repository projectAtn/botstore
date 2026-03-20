# OpenClaw Tool/Scope/Action Mapping (Phase 1)

Purpose: ensure sensitive actions are authorized with typed metadata before execution.

## Mapping schema
- `tool_name`
- `operation`
- `action_class`
- `requested_scope`
- `side_effect_level` (`read|write|external_send|delete|charge`)
- `auth_mode` (`none|per_install|per_call`)

## Initial mapping set
| tool | operation | action_class | requested_scope | side_effect_level | auth_mode |
|---|---|---|---|---|---|
| message.send | send | message.send | message.send | external_send | per_call |
| nodes.run | command | device.command | device.command | write | per_call |
| nodes.invoke | invoke | device.invoke | device.invoke | write | per_call |
| browser.act | click/type/submit | browser.act | browser.act | write | per_call |
| exec | command | shell.exec | shell.exec | write | per_call |

## Policy requirement
- `email.send`, `message.send`, `social.post`, `payment.charge`, `files.delete` are sensitive scopes.
- Any attempt to execute a sensitive action must call `/agent/action-authorize` first.

## Enforcement rules
1. Resolve mapping before tool execution.
2. If mapping is unknown for a side-effecting tool, fail closed.
3. For sensitive scopes, deny on missing grant or denied decision.
4. Emit action observation and include observed scopes in outcome-v2.

## Non-goals in phase 1
- Inferring sensitive scopes from free-form shell strings.
- Allowing raw browser automation for sensitive production actions.
