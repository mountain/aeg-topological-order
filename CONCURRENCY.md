# Concurrency Guardrails

These are soft research guardrails rather than hard limits. The purpose is to keep the Fibonacci reconstruction auditable and to prevent multiple agents from silently choosing incompatible gauges, normalizations, or categorical conventions.

## Default concurrency

- Default to **one primary topological-order research workstream**.
- A second concurrent workstream is acceptable when the tasks are genuinely independent, such as history-complex construction vs. a direct categorical baseline solver.
- Treat **two concurrent workstreams as the normal soft cap** for this repository.
- If `mountain/three-body` and `mountain/aeg-bianchi-ix` are already active in parallel sessions, assume the wider research program is sufficiently concurrent and avoid additional fan-out unless there is a strong reason.

## Single-writer rule

- Only one workstream at a time should modify canonical state: `STATUS.md`, the allowed-input list for blind reconstruction, gauge conventions, theorem/benchmark ledgers, and shared notation.
- Parallel workstreams should write separate notes, implementations, or audit reports until they are reconciled.
- Do not let an agent with access to known Fibonacci `F/R` values edit the blind-reconstruction derivation before the comparison gate is opened.

## Good parallel splits

Examples:

- history-complex generator vs. independent categorical baseline;
- pentagon-equation solver vs. exact solution verifier;
- representation-complexity benchmark vs. literature/originality audit.

Avoid running several agents that independently choose gauges or solve the same `F/R` system without a predefined comparison protocol.

## Expansion rule

Before exceeding two active workstreams, record:

1. the independent question assigned to each workstream;
2. file ownership;
3. frozen fusion/gauge conventions;
4. how outputs will be compared and reconciled.

Prefer one primary reconstruction plus one independent verifier over broad parallel search.
