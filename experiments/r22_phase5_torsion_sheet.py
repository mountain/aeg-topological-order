"""Phase-5 facade for the second physical D-amplitude sheet.

The accepted sparse nonlinear compiler and provenance-based certificate tools
were written before the theorem audit found the second gauge-inequivalent
cross-D amplitude class.  Their only dependence on the D-amplitude class is the
lower-data provider called by ``r22_epsminus_final_kernel.parametric_quotient_data``.

This facade injects class-1 lower data into the *same* Phase-5 compiler rather
than copying or forking that compiler.  The patch is process-local and restored
in ``finally`` so class-0 semantics remain the default everywhere else.

Serial usage:

    python r22_phase5_torsion_sheet.py --component 7 --mask 0 --mode kernel
    python r22_phase5_torsion_sheet.py --component 7 --mask 0 --mode two-cell

The second command should be run only after the fresh kernel fingerprint has
been inspected.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager

import r22_epsminus_final_kernel as fk
import r22_epsminus_f_parametric as fp
import r22_epsminus_f_torsion_probe as tp
import r22_phase5_two_cell_certificate as tc


def torsion_lower_data(cid: int, mask: int):
    lower = tp.second_sheet_lower_data(cid, mask)
    return (
        lower["scalar"],
        lower["ddata"],
        lower["e_params"],
        lower["emats"],
        lower["droot"],
    )


@contextmanager
def second_sheet_provider():
    """Temporarily replace the shared Phase-4 lower-data provider by class 1."""
    old = fp.parametric_lower_data
    if fk.fp is not fp:
        raise AssertionError("final-kernel compiler does not share F-parametric module")
    fp.parametric_lower_data = torsion_lower_data
    try:
        yield
    finally:
        fp.parametric_lower_data = old


def compile_kernel(cid: int, mask: int):
    with second_sheet_provider():
        out = fk.compile_branch(cid, mask)
    out = dict(out)
    out["D_amplitude_class"] = 1
    print("TORSION_SHEET", {
        "component": cid,
        "mask": mask,
        "D_amplitude_class": 1,
        "F_linear_components": out["F_linear_components"],
        "kernel_variables": out["kernel_variables"],
        "raw_nonzero_final_entries": out["raw_nonzero_final_entries"],
        "unique_kernel_polynomials": out["unique_kernel_polynomials"],
        "term_count_profile": out["term_count_profile"],
        "total_degree_profile": out["total_degree_profile"],
        "F_degree_profile": out["F_degree_profile"],
        "constant_contradictions": out["constant_contradictions"],
    }, flush=True)
    return out


def verify_two_cell(cid: int, mask: int):
    with second_sheet_provider():
        out = tc.verify(cid, mask)
    out = dict(out)
    out["D_amplitude_class"] = 1
    print("TORSION_SHEET", out, flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", type=int, required=True)
    ap.add_argument("--mask", type=int, required=True)
    ap.add_argument("--mode", choices=("kernel", "two-cell"), required=True)
    args = ap.parse_args()

    if args.mode == "kernel":
        compile_kernel(args.component, args.mask)
    else:
        verify_two_cell(args.component, args.mask)


if __name__ == "__main__":
    main()
