"""Executable global theorem-case ledger for R(2,2).

This is a bookkeeping theorem gate, not a new nonlinear solve.  It connects the
already independently replayed quotient/classification gates into one finite
case tree and rejects any omission, overlap, duplicate physical deep branch, or
missing archived/executable terminal certificate.

The ledger has 44 top-level terminal leaves:

* 8 epsilon-plus scalar components, each discharged by the complete local-F
  character-sheet obstruction;
* 4 shallow epsilon-minus scalar components, each discharged by the complete
  2^4 local-chirality F obstruction;
* 32 deep physical branches = 4 scalar components x 4 Pauli chirality masks x
  2 gauge-inequivalent D-amplitude classes, each discharged at Phase 5.

No claim about a terminal leaf is derived here from a filename alone: the
referenced files are frozen archives/interfaces for theorem gates that have
separate successful exact Actions replays.  This script proves that those gates
cover the finite quotient tree exactly once.
"""
from __future__ import annotations

from itertools import product
from pathlib import Path

import r22_epsplus_local_f_obstruction as ep
import r22_epsminus_shallow_local_f_obstruction as sh
import r22_epsminus_d_trace as tr
import r22_epsminus_d_amplitude as da

ROOT = Path(__file__).resolve().parents[1]

EPS_PLUS = tuple(ep.EPS_PLUS)
SHALLOW = tuple(sh.SHALLOW)
DEEP = tuple(sh.DEEP)
MASKS = tuple(sh.DEEP_SURVIVOR_MASKS)
D_CLASSES = (0, 1)

# ---------------------------------------------------------------------------
# TWO-BIT PARAMETRISATION OF THE COMPLETE SCALAR QUOTIENT, AND THE DICHOTOMY.
#
# Both organising bits are SIGNS OF SINGLE SCALARS, and both are derived:
#
#     eps(c) = 0  iff  c is epsilon = +1        (r22_epsplus_local_f_obstruction)
#     chi(c) = +/-1 from the scalar at CHI_KEY  (r22_epsminus_shallow_... , sh.chi)
#
# and the 16 components split as
#
#     eps = +1                     8   local-F SINGULARITY   (det F^{XXX}_X = 0)
#     eps = -1, chi = +1           4   local-F SINGULARITY
#     eps = -1, chi = -1           4   WINDING at Phase 5
#
# with the leaf census 8 + 4 + 4*4*2 = 44.  The two obstruction types are dual in
# kind: a block that pentagon coherence requires to be invertible is forced
# singular (a multiplicative/rank obstruction, certified by a determinant
# identity), versus a system of amplitude ratios that must be consistent being
# infeasible (an additive/holonomy obstruction, certified by a circulation with
# non-trivial holonomy).  chi is a Z/2 datum -- rank one, the cheapest possible
# invariant -- while the deep obstruction is a Z/4 cycle holonomy; the case tree is
# therefore organised entirely by two Z/2 signs, and the only Z/4 structure in the
# whole theorem lives on the 32-leaf deep frontier.
# The assertions below make the parametrisation executable rather than prose.
# ---------------------------------------------------------------------------
ALL_COMPONENTS = tuple(range(len(ep.COMPONENT_REPS)))
assert len(ALL_COMPONENTS) == 16
assert set(EPS_PLUS) | set(SHALLOW) | set(DEEP) == set(ALL_COMPONENTS)
assert not (set(EPS_PLUS) & set(SHALLOW))
assert not (set(EPS_PLUS) & set(DEEP))
assert not (set(SHALLOW) & set(DEEP))
assert all(sh.chi(c) == +1 for c in SHALLOW)
assert all(sh.chi(c) == -1 for c in DEEP)
# eps and chi are independent: all four combinations occur
assert {(c in EPS_PLUS, sh.chi(c)) for c in ALL_COMPONENTS} == {
    (True, +1), (True, -1), (False, +1), (False, -1)}

OBSTRUCTION = {}
for _c in ALL_COMPONENTS:
    if _c in EPS_PLUS or _c in SHALLOW:
        OBSTRUCTION[_c] = "singularity"
    else:
        OBSTRUCTION[_c] = "winding"

N_SINGULARITY_LEAVES = len(EPS_PLUS) + len(SHALLOW)          # 12
N_WINDING_LEAVES = len(DEEP) * len(MASKS) * len(D_CLASSES)   # 32
assert N_SINGULARITY_LEAVES == 12
assert N_WINDING_LEAVES == 32
assert N_SINGULARITY_LEAVES + N_WINDING_LEAVES == 44

# The class-0 canonical chain has one component-level Phase-5 synthesis per
# deep scalar component; each synthesis contains all four masks.
CLASS0_CERT = {
    5: "notes/31-r22-component5-phase5-closure.md",
    7: "notes/41-r22-component7-phase5-closure.md",
    13: "notes/36-r22-component13-phase5-closure.md",
    15: "notes/42-r22-component15-phase5-closure.md",
}

# The theorem audit's second physical D sheet.  Component 13 was closed mask by
# mask because it was the last frontier; the others have component/group notes.
CLASS1_CERT = {
    (5, 0): "notes/50-r22-second-d-sheet-component5-phase5-closure.md",
    (5, 105): "notes/50-r22-second-d-sheet-component5-phase5-closure.md",
    (5, 150): "notes/50-r22-second-d-sheet-component5-phase5-closure.md",
    (5, 255): "notes/50-r22-second-d-sheet-component5-phase5-closure.md",
    (7, 0): "notes/48-r22-second-d-sheet-17plus4-phase5-closure.md",
    (7, 105): "notes/48-r22-second-d-sheet-17plus4-phase5-closure.md",
    (7, 150): "notes/48-r22-second-d-sheet-17plus4-phase5-closure.md",
    (7, 255): "notes/48-r22-second-d-sheet-17plus4-phase5-closure.md",
    (13, 0): "notes/51-r22-second-d-sheet-component13-mask0-phase5-closure.md",
    (13, 105): "notes/52-r22-second-d-sheet-component13-mask105-phase5-closure.md",
    (13, 150): "notes/53-r22-second-d-sheet-component13-mask150-phase5-closure.md",
    (13, 255): "notes/54-r22-second-d-sheet-component13-mask255-phase5-closure.md",
    (15, 0): "notes/48-r22-second-d-sheet-17plus4-phase5-closure.md",
    (15, 105): "notes/48-r22-second-d-sheet-17plus4-phase5-closure.md",
    (15, 150): "notes/48-r22-second-d-sheet-17plus4-phase5-closure.md",
    (15, 255): "notes/48-r22-second-d-sheet-17plus4-phase5-closure.md",
}

GLOBAL_GATE_FILES = (
    "experiments/r22_scalar_component_inventory.py",
    "experiments/r22_epsplus_local_f_obstruction.py",
    "experiments/r22_epsminus_shallow_local_f_obstruction.py",
    "experiments/r22_epsminus_seed_pauli_normal_form_audit.py",
    "experiments/r22_epsminus_d_trace.py",
    "experiments/r22_epsminus_d_amplitude_gauge_audit.py",
    "experiments/r22_epsminus_d_discrete_gauge_audit.py",
    "experiments/r22_epsminus_d_pauli_normalizer_audit.py",
    "notes/47-r22-second-d-sheet-phase4-closure.md",
    "notes/55-r22-second-d-sheet-phase5-closure.md",
    "notes/56-r22-pauli-seed-normal-form-completeness.md",
)


def require_paths(paths):
    missing = [p for p in paths if not (ROOT / p).is_file()]
    if missing:
        raise AssertionError(("missing theorem-gate artifacts", missing))


def main():
    # 1. Scalar quotient partition: all 16 components exactly once.
    scalar_ids = set(range(len(ep.COMPONENT_REPS)))
    if len(ep.COMPONENT_REPS) != 16 or len(set(ep.COMPONENT_REPS)) != 16:
        raise AssertionError(("scalar representative inventory changed", len(ep.COMPONENT_REPS)))

    parts = [set(EPS_PLUS), set(SHALLOW), set(DEEP)]
    if any(parts[i] & parts[j] for i in range(3) for j in range(i)):
        raise AssertionError(("scalar terminal/deep classes overlap", parts))
    if set().union(*parts) != scalar_ids:
        raise AssertionError(("scalar partition is not exhaustive", scalar_ids, parts))

    expected_eps_minus = set(SHALLOW) | set(DEEP)
    if set(tr.EPS_MINUS) != expected_eps_minus:
        raise AssertionError(("D trace epsilon-minus frontier mismatch", tr.EPS_MINUS, expected_eps_minus))

    # 2. Deep projective frontier: the independently audited modules must agree
    # on exactly the same four scalar components and four survivor masks.
    if tuple(da.FRONTIER_COMPONENTS) != DEEP:
        raise AssertionError(("D-amplitude scalar frontier mismatch", da.FRONTIER_COMPONENTS, DEEP))
    if tuple(da.SURVIVOR_MASKS) != MASKS:
        raise AssertionError(("D-amplitude chirality masks mismatch", da.SURVIVOR_MASKS, MASKS))
    if MASKS != (0, 105, 150, 255):
        raise AssertionError(("unexpected chirality survivor set", MASKS))

    # The Pauli-normal-form gate proves the 256-mask trace is projectively
    # exhaustive; this ledger records the quotient cardinality it feeds.
    seed_chirality_count = 2 ** len(tr.SPACES)
    if len(tr.SPACES) != 8 or seed_chirality_count != 256:
        raise AssertionError(("unexpected seed chirality space", len(tr.SPACES), seed_chirality_count))

    # 3. Exact physical deep leaves: 4 x 4 x 2 = 32 unique quotient classes.
    deep_leaves = tuple(product(DEEP, MASKS, D_CLASSES))
    if len(deep_leaves) != 32 or len(set(deep_leaves)) != 32:
        raise AssertionError(("bad physical deep leaf count", len(deep_leaves), len(set(deep_leaves))))

    # 4. Attach every deep leaf to exactly one frozen terminal certificate.
    terminal = {}
    for cid, mask, dclass in deep_leaves:
        if dclass == 0:
            if cid not in CLASS0_CERT:
                raise AssertionError(("missing class-0 component certificate", cid, mask))
            cert = CLASS0_CERT[cid]
        elif dclass == 1:
            key = (cid, mask)
            if key not in CLASS1_CERT:
                raise AssertionError(("missing class-1 branch certificate", key))
            cert = CLASS1_CERT[key]
        else:
            raise AssertionError(("unexpected D class", dclass))
        terminal[(cid, mask, dclass)] = cert

    if set(terminal) != set(deep_leaves):
        raise AssertionError(("terminal deep manifest is not exact", set(deep_leaves) - set(terminal), set(terminal) - set(deep_leaves)))

    # 5. The non-deep scalar leaves are also explicit terminal cases.
    top_leaves = []
    for cid in EPS_PLUS:
        top_leaves.append(("epsilon-plus-local-F", cid, "experiments/r22_epsplus_local_f_obstruction.py"))
    for cid in SHALLOW:
        top_leaves.append(("epsilon-minus-shallow-local-F", cid, "experiments/r22_epsminus_shallow_local_f_obstruction.py"))
    for leaf in deep_leaves:
        top_leaves.append(("epsilon-minus-deep-Phase5", leaf, terminal[leaf]))

    if len(top_leaves) != 44:
        raise AssertionError(("unexpected global terminal-leaf count", len(top_leaves)))

    # 6. Every referenced interface/archive exists in the checked-out theorem
    # branch.  Separate Actions runs establish the mathematical verdicts.
    require_paths(GLOBAL_GATE_FILES)
    require_paths(set(CLASS0_CERT.values()) | set(CLASS1_CERT.values()))
    require_paths([row[2] for row in top_leaves])

    print({
        "scalar_components": 16,
        "epsilon_plus_terminal_scalars": list(EPS_PLUS),
        "epsilon_minus_shallow_terminal_scalars": list(SHALLOW),
        "epsilon_minus_deep_scalars": list(DEEP),
        "pauli_seed_chirality_assignments_per_deep_scalar": seed_chirality_count,
        "deep_survivor_masks": list(MASKS),
        "physical_D_classes_per_survivor": list(D_CLASSES),
        "physical_deep_terminal_leaves": len(deep_leaves),
        "global_terminal_leaves": len(top_leaves),
    }, flush=True)

    for cid in DEEP:
        rows = [(mask, dclass, terminal[(cid, mask, dclass)]) for mask in MASKS for dclass in D_CLASSES]
        print({"deep_component": cid, "terminal_branches": rows}, flush=True)

    print(
        "RESULT: the finite theorem case tree is exhaustive and non-overlapping: 8 epsilon-plus local-F leaves + 4 shallow epsilon-minus local-F leaves + 32 deep physical Phase-5 leaves = 44 terminal leaves, each attached to a frozen certificate",
        flush=True,
    )


if __name__ == "__main__":
    main()
