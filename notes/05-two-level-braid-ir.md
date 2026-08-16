# Note 05 — Two-Level Braid IR: History Certificates vs Execution Blocks

**Status:** negative complexity benchmark / compiler design note  
**Date:** 2026-08-17

## Result

The braid stage now separates naturally into two representations.

### 1. History / proof IR

A nonlocal adjacent exchange in a fixed fusion chart is represented explicitly as

\[
F\;\to\;R\;\to\;F^{-1}.
\]

This form records:

- which reassociation chart was entered;
- which fusion channel the local exchange acted on;
- which F/R axioms justify the transport;
- the exact provenance of the compiled operator.

It is therefore suitable as an auditable certificate or source IR.

### 2. Execution IR

After verification, the same path should be precompiled to the local block

\[
F^{-1}RF.
\]

In the Fibonacci fusion-path basis every generator is a direct sum of scalar and at-most-\(2\times2\) blocks.

## Cost comparison

For one nontrivial two-dimensional local block applied to a vector:

- precompiled \(2\times2\) execution block: 4 multiplications + 2 additions;
- replayed history \(F\to R\to F^{-1}\): 10 multiplications + 4 additions.

Thus replaying history is not an execution-speed improvement. It costs a constant factor more once the local block has already been compiled.

`experiments/braid_ir_cost_model.py` verifies across Fibonacci fusion sectors through \(n=16\) that:

1. direct precompiled execution is never more expensive in this elementary arithmetic model;
2. with shared global templates, direct and history representations require the same number of local block references;
3. hence neither representation has an asymptotic metadata-size advantage at this stage.

Representative total-\(\tau\) interior generators give multiplication ratios near 2:

- \(n=6\): 12 direct vs 24 history;
- \(n=10\): 85 direct vs 175 history;
- \(n=14\): 585 direct vs 1209 history.

## Architectural consequence

The right architecture is therefore not

\[
\text{AEG history representation replaces categorical execution}.
\]

It is

\[
\boxed{
\text{history/proof IR}
\longrightarrow
\text{verified compilation}
\longrightarrow
\text{optimized fusion-path execution IR}.
}
\]

This is a narrower but more defensible potential contribution.

## Research interpretation

**NEGATIVE BENCHMARK.** No runtime or asymptotic storage advantage over an optimized direct categorical compiler has been demonstrated for braid generators.

**REFORMULATION.** The remaining possible value of the AEG layer is provenance, explicit rewrite history, incremental recompilation, proof-carrying local transformations, and auditable equivalence of compiled operators.

This shifts the next decisive benchmark to a setting where provenance and many-path recoupling are genuinely nontrivial: Levin--Wen/string-net plaquette compilation.
