# Status

## Current stage

`T9 R(2,2) THEOREM-CLOSURE AUDIT — FINITE CASE LEDGER CLOSED / FINAL CANONICAL SERIAL REPLAY NEXT`

The theorem-completeness work remains on draft PR `#12`, branch `agent/r22-theorem-closure`. No theorem promotion or merge is authorized yet.

## Closed theorem gates

1. **Scalar quotient:** exactly 16 A/B/C components modulo the full complex gauge torus.
2. **Immediate local obstructions:** all 8 epsilon-plus scalar components and shallow epsilon-minus components `4,6,12,14` are independently excluded.
3. **Pauli seed normal form:** original seed-only D pentagons are exactly `24 singleton + 24 pair`; across deep components `5,7,13,15`, all `96/96` singleton relations are `U^2=I` and all `96/96` pair relations are anticommutators. Hence every invertible seed triple is independently `GL_2(C)`-conjugate to `(X,Z,+/-Y)`. Actions run `32394416585`; archive `notes/56-r22-pauli-seed-normal-form-completeness.md`.
4. **Deep chirality census:** on each deep scalar component, the now-projectively-exhaustive `2^8=256` seed assignments reduce exactly to masks `0,105,150,255` with profile `192 structural + 60 phase + 4 survivors`.
5. **D-amplitude quotient:** exactly two gauge-inequivalent physical D-amplitude classes per deep chirality survivor. Thus the physical deep frontier is `4 x 4 x 2 = 32` branches.
6. **Phases 1–4:** all 32 physical deep branches have exact D witnesses and pass through Phase 4.
7. **Phase 5, D class 0:** accepted canonical chain closes all 16 branches.
8. **Phase 5, D class 1:** theorem audit closes all 16 branches. Full archive `notes/55-r22-second-d-sheet-phase5-closure.md`; final branch `component 13 / mask 255 / class 1` closes 18/18 finite strata in Actions run `32393826437`.
9. **Executable global case ledger:** the complete finite quotient tree is exact, exhaustive, and non-overlapping. Actions run `32394807045` verifies
   \[
   8\ \epsilon_+\text{ terminal leaves}
   +4\ \epsilon_-\text{ shallow terminal leaves}
   +32\ \epsilon_-\text{ deep physical terminal leaves}
   =44\text{ top-level terminal leaves}.
   \]
   Every deep leaf is exactly one triple
   \[
   (\text{scalar},\text{chirality mask},\text{D class})
   \in
   \{5,7,13,15\}\times\{0,105,150,255\}\times\{0,1\},
   \]
   and every leaf is attached to a frozen terminal certificate. Verifier `experiments/r22_theorem_case_ledger.py`; archive `notes/57-r22-global-theorem-case-ledger.md`.

## Current theorem boundary

The theorem audit has now closed all known **local algebra, projective-normal-form, gauge-component, chirality, D-amplitude, branch-completeness, and terminal-case bookkeeping gaps**.

In particular:

- the historical sign-only scalar-gauge issue is repaired by the full-complex scalar quotient;
- the previously missing second physical D-amplitude sheet is fully propagated and terminally obstructed;
- the historical Pauli seed choice is proved to be a complete `GL_2(C)` normal form, not an ansatz;
- the resulting global finite case tree contains exactly 44 terminal leaves with no omissions or duplicate physical quotient classes.

This is the point at which the research changes character: no additional branch search is currently justified. The remaining theorem gate is a fresh canonical replay of the already-frozen proof tree.

## Open frontier — final canonical serial replay

The final replay must begin from fresh checkout/state and reconstruct the theorem in serial sub-gates, each within the 10-minute Actions limit:

1. **Replay A — scalar/local frontier**
   - full-complex scalar component inventory;
   - epsilon-plus exhaustive local-F obstruction;
   - shallow epsilon-minus local-F obstruction.

2. **Replay B — deep projective/gauge frontier**
   - Pauli seed normal-form completeness;
   - all four deep `256 -> 4` chirality traces;
   - cross-D amplitude Smith/gauge audit proving exactly two physical D classes.

3. **Replay C — downstream existence frontier**
   - both D classes exact at D;
   - E and F/Phase-4 replay for every retained branch.

4. **Replay D — terminal frontier**
   - class-0 Phase-5 certificates;
   - class-1 Phase-5 certificates;
   - require terminal branch IDs/counts to agree with the executable 44-leaf ledger.

Only after all replay sub-gates succeed on the same frozen theorem branch should the repository write the theorem-level synthesis and decide whether to promote
\[
\boxed{R(2,2)\text{ is non-categorifiable}.}
\]

## Verification discipline

- full-complex gauge, not sign-only gauge;
- exact Smith/lattice calculations for monomial components;
- source-provenance terminal certificates;
- localization only after nonzeroness is proved;
- no global Gröbner solve;
- no floating-point nonlinear solve or continuation;
- 10-minute maximum per Actions research job;
- split replay stages rather than increasing timeouts;
- named `z_j` coordinates are implementation charts, not invariant theorem evidence.
