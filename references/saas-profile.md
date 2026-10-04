# F4A SaaS Profile

Use for web applications, APIs, business workflows, subscriptions, accounts, and typical cloud services.

## Default architecture

- Prefer a modular monolith during validation unless independent scaling, isolation, or ownership justifies distribution.
- Organize primarily by business domain, not by pages or a universal technical-layer tree.
- Keep domain rules independent of web frameworks, ORMs, model SDKs, payment SDKs, and email providers.
- Put external systems behind explicit adapters or providers.
- Treat AI as an uncertain external dependency, not a source of business truth.
- Validate AI output with schemas, permissions, and domain rules before persistence or action.

Example shape, not a mandatory tree:

```text
src/
  modules/
    identity/
    workspace/
    billing/
    core-domain/
    workflow/
    ai/
    integrations/
  infrastructure/
  shared/
  app/
```

## Dependency direction

```text
UI / API / Worker
        ↓
Application / Workflow
        ↓
Domain Rules
        ↑
Infrastructure Adapters
```

Infrastructure implements contracts needed by the application/domain. The domain does not know which database, web framework, payment provider, or model vendor is used.

## Quality gates

For a standard or higher-risk feature, verify as relevant:

- user story, non-goals, and acceptance criteria;
- server-authoritative validation and permission enforcement;
- success, empty, failure, and permission paths;
- migration, compatibility, and rollback for data changes;
- idempotency and concurrency where duplicate execution is possible;
- cost, rate limits, schema validation, and human approval for AI actions;
- minimum observability for the user journey;
- no regression to the main user path;
- an ADR for consequential, costly-to-reverse choices.

Do not add layers, services, queues, or abstractions merely to make the architecture look complete.
