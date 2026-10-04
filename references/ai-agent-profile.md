# F4A AI Agent Profile

Use for systems that plan, call tools, retain memory, delegate work, or take actions with partial autonomy.

## Boundaries

- Separate user intent, planning, tool execution, durable memory, and result verification.
- Treat model output as proposed data or action, never implicit authorization.
- Give every tool an explicit input/output contract and least-privilege scope.
- Require user approval immediately before material external, destructive, financial, or irreversible actions unless prior authority clearly covers them.
- Keep untrusted tool and retrieved content separate from instructions.

## Reliability

- Validate structured output against schemas.
- Define retry limits and stopping conditions.
- Make idempotency and duplicate-action handling explicit.
- Record provenance for important facts and actions.
- Test prompt injection, missing data, tool failure, stale memory, and partial completion.
- Use deterministic checks for permissions, policy, calculations, and final acceptance wherever possible.

## Evaluation

Define task-specific datasets and acceptance criteria. Track success, unsafe action rate, human correction rate, cost, latency, and regressions. Do not advertise a universal Pass@1 target without a maintained benchmark, sample size, and baseline.
