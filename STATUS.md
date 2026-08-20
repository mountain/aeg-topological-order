# Status

## Current stage

`T9 R(2,2) THEOREM-CLOSURE AUDIT — FULL SCALAR INVENTORY CLOSED / TWO PHYSICAL D-AMPLITUDE SHEETS ESTABLISHED / SECOND SHEET 12 OF 16 PHASE-5 BRANCHES CLOSED`

Canonical checkpoints on the accepted/class-0 chain:

- Phase 1–4: `notes/23-r22-phases1-4-closure.md`;
- component 5 Phase 5: `notes/31-r22-component5-phase5-closure.md`;
- component 13 Phase 5: `notes/36-r22-component13-phase5-closure.md`;
- component 7 Phase 5: `notes/41-r22-component7-phase5-closure.md`;
- component 15 Phase 5: `notes/42-r22-component15-phase5-closure.md`.

Theorem-audit checkpoints:

- shallow epsilon-minus executable closure: `notes/43-r22-shallow-epsminus-local-f-closure.md`;
- full complex-gauge scalar inventory: `notes/44-r22-scalar-component-inventory-audit.md`;
- D-amplitude mod-gauge frontier: `notes/45-r22-d-amplitude-mod-gauge-frontier.md`;
- second-sheet Phase-3 closure: `notes/46-r22-second-d-sheet-e-layer-closure.md`;
- second-sheet Phase-4 closure: `notes/47-r22-second-d-sheet-phase4-closure.md`;
- second-sheet components 7/15 Phase-5 closure: `notes/48-r22-second-d-sheet-17plus4-phase5-closure.md`;
- second-sheet component 5 mask-0 closure: `notes/49-r22-second-d-sheet-component5-mask0-phase5-closure.md`;
- second-sheet complete component-5 closure: `notes/50-r22-second-d-sheet-component5-phase5-closure.md`.

## Theorem boundary

The target is categorifiability of the Meng–Yu rank-six self-dual fusion ring `R(2,2)`.

The full scalar A/B/C inventory has been re-audited modulo the **full complex gauge torus**. There are exactly 16 scalar components, split as

\[
\epsilon_+:\quad 0,1,2,3,8,9,10,11,
\]

\[
\epsilon_-:\quad 4,5,6,7,12,13,14,15.
\]

The epsilon-plus half is independently excluded by the exhaustive local-F determinant census. The shallow epsilon-minus components

\[
4,6,12,14
\]

have independent executable local-F obstruction certificates.

The deep epsilon-minus components are

\[
\boxed{5,7,13,15}.
\]

Phase 1 exhausts 256 chirality masks to exactly

\[
\boxed{0,105,150,255}
\]

for each deep scalar component.

## Critical theorem-audit correction — two physical D-amplitude sheets

The theorem audit found that the historical Phase-2 D-amplitude engine selected one exact witness but did not prove uniqueness modulo residual gauge.

The exact homogeneous cross-D amplitude group is

\[
H_D\cong(\mathbf C^*)^6\times\mu_2\times\mu_2.
\]

The connected six-dimensional part is pure residual gauge. The disconnected scalar residual gauge removes one of the two `Z2` factors, while the Pauli normalizer contributes no additional discrete identification. Therefore one genuine physical `Z2` remains:

\[
\boxed{\text{two gauge-inequivalent D-amplitude classes per deep chirality branch}.}
\]

The deep theorem frontier is consequently

\[
4\text{ scalar components}\times4\text{ chirality masks}\times2\text{ D classes}=32
\]

rather than the previously assumed 16 branches.

Both classes have exact D witnesses and replay all original D pentagons. All 32 branches pass Phases 1–4.

## Second D-amplitude sheet — current Phase-5 ledger

For D-amplitude class `1`:

\[
\boxed{5:4/4\ \text{CLOSED}},
\]

\[
\boxed{7:4/4\ \text{CLOSED}},
\]

\[
\boxed{15:4/4\ \text{CLOSED}}.
\]

Thus

\[
\boxed{12/16}
\]

second-sheet Phase-5 branches are `CLOSED / EXACT`.

The only remaining second-sheet branches are

\[
\boxed{
13/0,\quad13/105,\quad13/150,\quad13/255.
}
\]

### Component 5 class-1 closure

Every component-5 class-1 mask has:

- 21 active weighted F components;
- 23 nonlinear variables;
- 50,880 raw nonzero final entries;
- 219 unique cubic relations;
- exact finite reduction to 18 `(p,q,z0)` strata;
- the universal affine split
  \[
  \boxed{18=10_{\rm rank11}+8_{\rm rank10}};
  \]
- a two-variable rank-drop core in `x=z19`, `y=z20`;
- complete few-cell source certificates for all eight rank-drop strata.

Masks `105` and `150` are particularly uniform: the same fixed source family

```text
(XXXX;g)_(0,2)
(XXXX;g)_(0,3)
(XXXXX)_(2,23)
```

closes every one of their rank-10 branches. Mask `255` closes four branches by an exact resultant `-48*y^4` and four by a sign split. Full synthesis: `notes/50-r22-second-d-sheet-component5-phase5-closure.md`.

## Verification-method correction

A historical named-coordinate stability probe could relabel weighted-F quotient coordinates between independent constructions. Named `z_j` identities are therefore not theorem evidence by themselves.

Where possible, theorem-level certificates are now stated by final-pentagon **source provenance** and algebraic relation. Components `7` and `15` use a coordinate-free two-cell verifier that dynamically discovers the active scale coordinate from the first source cell.

The component-5 second-sheet proof likewise source-validates every decisive local cell after a fresh quotient construction.

## Open frontier — theorem closure

The highest-priority research node is now

\[
\boxed{\text{scalar component 13 / D-amplitude class 1 / masks }0,105,150,255.}
\]

Component `13` is a 21-active-F Phase-4 type like component `5`, but no component-5 finite-scale coordinate, relation, or certificate is authorized as an assumption. Each mask must be fresh source-replayed.

After component `13` class `1` is closed or otherwise resolved, the remaining theorem work is:

1. audit seed-scalar normalization into the exact Pauli/projective normal form;
2. freeze the exhaustive 16-scalar -> chirality -> two-D-sheet -> terminal-obstruction case ledger;
3. perform the final canonical serial replay from fresh state;
4. write the theorem-level synthesis;
5. only then decide whether to promote
   \[
   \boxed{R(2,2)\text{ is non-categorifiable}.}
   \]

No global Gröbner computation, floating-point nonlinear search, or timeout increase is authorized before small exact local structure is exhausted. The 10-minute per-job guardrail remains in force.

## SCM boundary

`main` records accepted, reproducible research state. The theorem-completeness work remains on draft PR `#12`, branch `agent/r22-theorem-closure`, until the global case ledger and final replay are complete.
