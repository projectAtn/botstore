# BotStore GitHub Integration Matrix (v1)

Scoring: 1 (low) to 5 (high)
- **Impact**: strategic value for BotStore plugin ecosystem
- **Effort**: implementation complexity/time
- **Risk**: security/operational/legal risk
- **Priority Score**: `Impact*2 - Effort - Risk` (higher is better)

| Repo | Impact | Effort | Risk | Priority Score | Why it matters |
|---|---:|---:|---:|---:|---|
| CopilotKit/CopilotKit | 5 | 3 | 2 | 5 | Great patterns for in-app agent UX and command/action surfaces. |
| activepieces/activepieces | 5 | 4 | 3 | 3 | Strong connector/action schema inspiration for skills/plugins. |
| e2b-dev/E2B | 4 | 3 | 2 | 3 | Sandbox execution model for safer pack testing and isolation. |
| trycua/cua | 4 | 4 | 3 | 1 | Computer-use infra patterns, useful for advanced browser/tool skills. |
| alibaba/OpenSandbox | 4 | 4 | 3 | 1 | Scalable sandbox/eval architecture reference. |
| zhayujie/chatgpt-on-wechat | 3 | 2 | 2 | 2 | Messaging channel bridge patterns for user-facing plugin flows. |
| crestalnetwork/intentkit | 3 | 4 | 3 | -1 | Multi-agent cluster ideas, but heavy architecture lift. |
| Integuru-AI/Integuru | 3 | 4 | 4 | -2 | Integration automation concepts; high governance risk if unguarded. |

## First 3 PoCs to build now
1. **CopilotKit adapter PoC**
   - Goal: expose BotStore search/install actions in app-native assistant surfaces.
2. **Activepieces adapter PoC**
   - Goal: map BotStore pack capabilities to action/trigger-style connector blocks.
3. **E2B sandbox adapter PoC**
   - Goal: run pack smoke checks in isolated execution context before promotion.

## Success criteria (PoC phase)
- Each adapter can perform: search -> install request -> activation status check.
- Adapter can return clear errors and policy/approval status.
- At least one end-to-end demo flow per adapter documented.
