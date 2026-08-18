"""Parent-local continuation-mass PAL probe for the closed epsilon-plus R(2,2) family.

This is an auxiliary SOFT-ORDERING experiment only.  It never enters the hard
pentagon proof or any certified prune decision.

Compared with r22_pal_distance_probe.py, this replay restores the successful PAL
training geometry used in the domino/X3C work: parent-local listwise supervision.
For one scalar component, view a projective branch as a two-step construction

    component -> even-parity K4 gluing A0 -> odd-parity K4 gluing A1.

The already-frozen local-F rank proxy defines a nonzero terminal utility even
though every epsilon-plus branch is exactly obstructed:

    utility(A0,A1) = exp(-(10-r_probe(A0,A1))/2).

For each parent (component,A0), the exact soft continuation mass is

    H(A0) = sum_A1 utility(A0,A1),

and the child teacher is the conditional distribution

    q(A1 | component,A0) = utility(A0,A1) / H(A0).

Thus the experiment tests the same parent-normalized construction principle as
PAL's completion-mass distillation, rather than pointwise binary classification.
The transfer split is across entire scalar components.
"""
from __future__ import annotations

import argparse
from collections import defaultdict

import numpy as np

import r22_pal_distance_probe as base

try:
    import torch
    import torch.nn.functional as F
except Exception as exc:  # pragma: no cover
    raise SystemExit("torch is required for the PAL continuation-mass probe") from exc


N_GLUINGS = 52
TRAIN_COMPONENTS = tuple(sorted(base.TRAIN_COMPONENTS))
TEST_COMPONENTS = tuple(sorted(base.TEST_COMPONENTS))


def component_blocks(X, ranks, cids):
    """Return cid -> (52,52,feature_dim), ranks (52,52)."""
    out = {}
    for cid in sorted(set(int(x) for x in cids)):
        sel = np.flatnonzero(cids == cid)
        assert len(sel) == N_GLUINGS * N_GLUINGS
        # build_dataset orders branches with A0 outer, A1 inner.
        out[cid] = (
            X[sel].reshape(N_GLUINGS, N_GLUINGS, X.shape[1]),
            ranks[sel].reshape(N_GLUINGS, N_GLUINGS),
        )
    return out


def make_groups(blocks, components, beta: float = 0.5):
    groups = []
    for cid in components:
        Xc, Rc = blocks[cid]
        Uc = np.exp(-beta * (10.0 - Rc)).astype(np.float32)
        for i in range(N_GLUINGS):
            u = Uc[i]
            mass = float(u.sum())
            assert mass > 0
            q = u / mass
            groups.append(
                {
                    "cid": cid,
                    "a0": i,
                    "X": Xc[i].astype(np.float32),
                    "ranks": Rc[i].astype(np.float32),
                    "utility": u,
                    "q": q.astype(np.float32),
                    "H": mass,
                }
            )
    return groups


def stack_groups(groups):
    X = np.stack([g["X"] for g in groups])
    q = np.stack([g["q"] for g in groups])
    return torch.tensor(X), torch.tensor(q)


def train_listwise(model_cls, groups, seed: int, steps: int, lr: float, tau: float):
    model = model_cls(groups[0]["X"].shape[1], seed=seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    X, q = stack_groups(groups)
    G, C, D = X.shape
    for _ in range(steps):
        opt.zero_grad()
        scores = model(X.reshape(G * C, D)).reshape(G, C) / tau
        logp = torch.log_softmax(scores, dim=1)
        loss = -(q * logp).sum(dim=1).mean()
        loss.backward()
        opt.step()
    return model


def _projective_and_radius(model, Xflat):
    """Expose PAL [z] and rho for theory diagnostics; None for ordinary MLP."""
    if not isinstance(model, base.PALSoft):
        return None, None
    with torch.no_grad():
        out = model.enc(torch.tensor(Xflat))
        d = model.d
        zr = out[:, :d]
        zi = out[:, d:2*d]
        rho = F.softplus(out[:, -1]) + 1e-3
        z = torch.complex(zr, zi)
        z = z / (torch.linalg.vector_norm(z, dim=1, keepdim=True) + 1e-12)
    return z.cpu().numpy(), rho.cpu().numpy()


def spearman(a, b):
    return base.spearman(np.asarray(a), np.asarray(b))


def evaluate(model, groups, tau: float):
    mass1 = []
    mass5 = []
    mass10 = []
    rank1 = []
    rank9_1 = []
    best_pos = []
    kl = []
    nll = []
    uniform_mass1 = []
    oracle_mass1 = []
    H = []
    rho_all = []
    logu_all = []

    for g in groups:
        X = torch.tensor(g["X"])
        with torch.no_grad():
            s = model(X).cpu().numpy()
        order = np.argsort(-s)
        q = g["q"].astype(np.float64)
        ranks = g["ranks"]

        mass1.append(float(q[order[:1]].sum()))
        mass5.append(float(q[order[:5]].sum()))
        mass10.append(float(q[order[:10]].sum()))
        rank1.append(float(ranks[order[0]]))
        rank9_1.append(float(ranks[order[0]] == 9))
        deepest = float(ranks.max())
        best_pos.append(1 + min(int(k) for k, j in enumerate(order) if ranks[j] == deepest))

        st = s / tau
        st = st - st.max()
        p = np.exp(st); p /= p.sum()
        nz = q > 0
        kl.append(float(np.sum(q[nz] * (np.log(q[nz]) - np.log(p[nz] + 1e-30)))))
        nll.append(float(-np.sum(q[nz] * np.log(p[nz] + 1e-30))))
        uniform_mass1.append(1.0 / len(q))
        oracle_mass1.append(float(q.max()))
        H.append(g["H"])

        _z, rho = _projective_and_radius(model, g["X"])
        if rho is not None:
            rho_all.extend(rho.tolist())
            logu_all.extend(np.log(g["utility"] + 1e-12).tolist())

    ans = {
        "mass@1": float(np.mean(mass1)),
        "mass@5": float(np.mean(mass5)),
        "mass@10": float(np.mean(mass10)),
        "top1_mean_rank": float(np.mean(rank1)),
        "top1_rank9_fraction": float(np.mean(rank9_1)),
        "branches_before_deepest": float(np.mean(best_pos)),
        "teacher_KL": float(np.mean(kl)),
        "teacher_cross_entropy": float(np.mean(nll)),
        "uniform_mass@1": float(np.mean(uniform_mass1)),
        "oracle_mass@1": float(np.mean(oracle_mass1)),
        "mean_parent_H": float(np.mean(H)),
    }
    if rho_all:
        ans["rho_vs_log_terminal_utility_spearman"] = spearman(rho_all, logu_all)
    return ans


def summarize(rows):
    by = defaultdict(list)
    for r in rows:
        for k, v in r.items():
            by[k].append(v)
    return {k: (float(np.mean(v)), float(np.std(v))) for k, v in by.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--lr", type=float, default=7e-3)
    ap.add_argument("--tau", type=float, default=1.0)
    ap.add_argument("--beta", type=float, default=0.5)
    args = ap.parse_args()

    X, ranks, cids, profiles = base.build_dataset()
    blocks = component_blocks(X, ranks, cids)
    train_groups = make_groups(blocks, TRAIN_COMPONENTS, beta=args.beta)
    test_groups = make_groups(blocks, TEST_COMPONENTS, beta=args.beta)

    print("train components", TRAIN_COMPONENTS, "groups", len(train_groups))
    print("test components", TEST_COMPONENTS, "groups", len(test_groups))
    print("children per group", N_GLUINGS)
    print("binary theorem positives: 0 (all epsilon-plus branches are exactly obstructed)")

    results = {}
    for name, cls in (("PAL-mass", base.PALSoft), ("MLP-mass", base.RealMLP)):
        rows = []
        for k in range(args.seeds):
            model = train_listwise(
                cls, train_groups, seed=700 + k,
                steps=args.steps, lr=args.lr, tau=args.tau,
            )
            rows.append(evaluate(model, test_groups, tau=args.tau))
        results[name] = summarize(rows)

    for name, stats in results.items():
        print(name)
        for key, (mean, sd) in stats.items():
            print(f"  {key}: {mean:.6f} +/- {sd:.6f}")

    print("NOTE: learned scores are soft ordering only; exact pentagons remain authoritative.")


if __name__ == "__main__":
    main()
