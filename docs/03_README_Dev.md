# F4A Developer Guide

## Before implementation

1. Read repository instructions and the relevant specification.
2. Identify the deployable subsystem and its Primary Profile.
3. Confirm risk level, non-goals, acceptance criteria, and required evidence.
4. Read only the relevant Profile reference.

## During implementation

- Keep the change within its declared scope.
- Preserve profile-specific dependency and trust boundaries.
- Treat AI-generated output as a proposal requiring validation.
- Do not introduce unrelated architecture, abstraction, or refactoring.
- Record an ADR only for consequential or costly-to-reverse decisions.

## Before completion

- Verify the main path and risk-relevant failure paths.
- Confirm permissions, migration/rollback, recovery, observability, or hardware evidence where applicable.
- State what was measured, what remains assumed, and what could not be verified.
- Update durable documents when implementation changes a boundary or decision.
