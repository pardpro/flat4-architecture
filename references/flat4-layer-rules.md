# Legacy Flat-4 Layer Rules

This is the optional layer convention for Hardware / Realtime subsystems that benefit from strict dependency control. It is not F4A Core and is not the default SaaS structure.

## Layer map

| Layer | Responsibility | May call |
| --- | --- | --- |
| L0 Domain | Pure state, rules, algorithms | Utils |
| L1 Entry | Request/protocol entry and routing | L2; L4 only for demonstrably side-effect-free simple queries; Utils |
| L2 Coordinator | Context, state machine, retry, timeout, rollback | L0, L3, L4, Utils, injected policies |
| L3 Molecular | Reusable stateless sequence of L4 operations | L4, Utils |
| L4 Atomic | One isolated external or runtime operation | Utils |
| Utils | Business-independent pure technical helpers | Utils |

Same-layer and reverse calls are prohibited except between Utils. L3 remains optional.

## Important limits

- `L1 -> L4` cannot be proven safe from import direction alone; review query semantics and side effects.
- L0 purity requires semantic review for I/O and hidden state.
- Zero-allocation, lock freedom, latency, temperature, power, and scheduling are optional product contracts that require runtime evidence.
- Run `scripts/validate_flat4.py` only as a static dependency screen. A pass is not architectural certification.
