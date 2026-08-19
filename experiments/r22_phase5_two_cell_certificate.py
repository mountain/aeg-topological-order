"""Coordinate-free exact two-cell certificate for Phase-5 scalar components.

For a fresh (component, chirality-mask) Phase-5 kernel, inspect two fixed
final-pentagon cells by provenance rather than by a hard-coded z_j name:

    (X,X,X,X,X)_(0,0)  -> s = 0
    (X,X,X,X,1)_(0,0)  -> s^2 - 1/2 = 0

Here ``s`` is discovered from the freshly compiled first cell.  This makes the
certificate invariant under implementation-dependent permutations of the
active F-component coordinates.

No Groebner basis or nonlinear solve is used.
"""
from __future__ import annotations

import argparse
import sympy as sp

import r22_phase5_monomial_lift as ml

P1 = (("X", "X", "X", "X", "X"), (0, 0))
P2 = (("X", "X", "X", "X", "1"), (0, 0))
P, Q = sp.symbols("p q")
ZS = sp.symbols("z0:32")


def coeff_expr(gc):
    (ar, ad), (br, bd) = gc
    return sp.Rational(ar, ad) + sp.I * sp.Rational(br, bd)


def expr_from_key(key, variables):
    out = sp.Integer(0)
    for mon, gc in key:
        if len(mon) != len(variables):
            raise AssertionError(("monomial arity mismatch", len(mon), len(variables)))
        term = coeff_expr(gc)
        for var, exp in zip(variables, mon):
            if exp:
                term *= var ** exp
        out += term
    return sp.expand(out)


def monic_expr(expr, variables):
    poly = sp.Poly(sp.expand(expr), *variables, extension=[sp.I])
    if poly.is_zero:
        raise AssertionError("unexpected zero polynomial")
    return sp.expand(poly.monic().as_expr())


def verify(component, mask):
    quotient, unique = ml.compile_unique(component, mask)
    nvars = quotient["nvars"]
    if nvars < 3 or nvars > 2 + len(ZS):
        raise AssertionError(("unexpected variable count", nvars))
    variables = (P, Q) + ZS[: nvars - 2]
    by_prov = {prov: key for key, prov in unique.items()}
    for prov in (P1, P2):
        if prov not in by_prov:
            raise AssertionError(("missing provenance", prov))

    e1 = monic_expr(expr_from_key(by_prov[P1], variables), variables)
    e2 = monic_expr(expr_from_key(by_prov[P2], variables), variables)

    # The first fixed cell must be one active F coordinate, with no p/q factor.
    p1 = sp.Poly(e1, *variables, extension=[sp.I])
    terms1 = p1.terms()
    if len(terms1) != 1 or p1.total_degree() != 1:
        raise AssertionError(("P1 is not a linear monomial", e1))
    powers1, coeff1 = terms1[0]
    if coeff1 != 1:
        raise AssertionError(("P1 not monic", e1))
    active_positions = [i for i, power in enumerate(powers1) if power]
    if len(active_positions) != 1 or powers1[active_positions[0]] != 1:
        raise AssertionError(("P1 not a single coordinate", e1))
    pos = active_positions[0]
    if pos < 2:
        raise AssertionError(("P1 unexpectedly uses E-torus parameter", e1))
    scale = variables[pos]

    expected2 = monic_expr(scale**2 - sp.Rational(1, 2), variables)
    if e2 != expected2:
        raise AssertionError(("P2 mismatch", "scale", str(scale), "P1", e1, "P2", e2))

    contradiction = sp.expand(e2.subs(scale, 0))
    if contradiction != -sp.Rational(1, 2):
        raise AssertionError(("unexpected contradiction", contradiction))

    out = {
        "component": component,
        "mask": mask,
        "scale": str(scale),
        "kernel_variables": nvars,
        "unique_kernel_polynomials": len(unique),
        "P1": str(e1),
        "P2": str(e2),
        "contradiction": str(contradiction),
        "closed": True,
    }
    print(out, flush=True)
    print(
        "RESULT: excluded by coordinate-free two-cell source certificate",
        flush=True,
    )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, required=True)
    ap.add_argument("--mask", type=int, required=True)
    args = ap.parse_args()
    verify(args.component, args.mask)


if __name__ == "__main__":
    main()
