"""PAL sidecar probe for the already-closed epsilon=+1 R(2,2) branch family.

This experiment never participates in hard pruning or in the proof path.  It
uses the exact epsilon-plus local-F branch enumerator only to generate a graded
soft teacher: a finite-field rank-proximity diagnostic for the required
10x10 F^{XXX}_X block.

Motivation: the exact theorem target `det != 0` has zero positives on all 21632
epsilon-plus branches, so binary supervision is degenerate.  We instead define

    d = 10 - r_probe,
    y = exp(-d / 2),

where r_probe is the maximum rank seen under two deterministic nonzero
assignments to the weighted-component parameters over a large prime field.
This teacher is for search-policy learning only; it is not a characteristic-zero
mathematical certificate.  The exact determinant-zero proof remains in
r22_epsplus_local_f_obstruction.py.

The model copied in miniature here follows the Complex-Hermitian PAL-II geometry
from mountain/domino-tiling/paltorus/pal/model.py:

    state encoder -> z in C^d and rho > 0
    predicate      -> c in C^d
    q              = |c^dag z|^2 / (||c||^2 ||z||^2)

A same-hidden-width real MLP is the baseline.

Default transfer split:
    train scalar components {0,1,8,9}
    test  scalar components {2,3,10,11}

Only branch/history features and the C-layer scalar signs are given to the
models.  No local-F equation, rank, forced-zero count, or obstruction feature
is an input.
"""
from __future__ import annotations

import argparse
import math
import random
from collections import Counter

import numpy as np

import r22_epsplus_local_f_obstruction as ex

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except Exception as exc:  # pragma: no cover
    raise SystemExit("torch is required for the PAL sidecar probe") from exc


PRIME = 1_000_003
TRAIN_COMPONENTS = {0, 1, 8, 9}
TEST_COMPONENTS = {2, 3, 10, 11}


def mod_rank(mat, p: int = PRIME) -> int:
    A = [[int(x) % p for x in row] for row in mat]
    m, n = len(A), len(A[0])
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i][c]), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(v * inv) % p for v in A[r]]
        for i in range(m):
            if i == r or not A[i][c]:
                continue
            fac = A[i][c]
            A[i] = [(A[i][j] - fac * A[r][j]) % p for j in range(n)]
        r += 1
        if r == m:
            break
    return r


def rank_probe(rows, seed: int, trials: int = 2, p: int = PRIME) -> int:
    """Soft teacher only: max finite-field rank over deterministic probes."""
    uf, forced = ex.analyze_rows(rows)
    roots = sorted({uf.find(i)[0] for i in range(100)} - forced)
    ridx = {r: j for j, r in enumerate(roots)}
    rng = random.Random(seed)
    best = 0
    for _ in range(trials):
        vals = [rng.randrange(1, p) for _ in roots]
        mat = []
        for i in range(10):
            rr = []
            for j in range(10):
                root, w = uf.find(10 * i + j)
                if root in forced:
                    rr.append(0)
                    continue
                num = int(w.numerator) % p
                den = int(w.denominator) % p
                coeff = num * pow(den, p - 2, p) % p
                rr.append(coeff * vals[ridx[root]] % p)
            mat.append(rr)
        best = max(best, mod_rank(mat, p))
    return best


def cbits(ch: int) -> np.ndarray:
    return np.asarray([(ch >> i) & 1 for i in range(3)], dtype=np.float32)


def branch_features(A0, A1) -> np.ndarray:
    """Sheet-swap invariant branch features; no verifier-derived values."""
    A = {**A0, **A1}
    v0 = sorted(A0)
    v1 = sorted(A1)
    out: list[float] = []
    for v in v0 + v1:
        a, b = A[v]
        ba, bb = cbits(a), cbits(b)
        out.extend(((ba + bb) / 2.0).tolist())
        out.extend(np.abs(ba - bb).tolist())
    for vv in (v0, v1):
        weights, distances = [], []
        for v in vv:
            a, b = A[v]
            weights.extend([float(cbits(a).sum()), float(cbits(b).sum())])
            distances.append(float(np.abs(cbits(a) - cbits(b)).sum()))
        out.extend([float(np.mean(weights) / 3.0), float(np.mean(distances) / 3.0)])
    return np.asarray(out, dtype=np.float32)


C_INDICES = [i for i, k in enumerate(ex.SC_KEYS) if ex.f_class(k) == "C"]
assert len(C_INDICES) == 72


def scalar_c_features(cid: int) -> np.ndarray:
    bits = ex.COMPONENT_REPS[cid]
    return np.asarray(
        [1.0 if ((bits >> i) & 1) == 0 else -1.0 for i in C_INDICES],
        dtype=np.float32,
    )


def build_dataset():
    base_feats = []
    branch_ids = []
    for i, A0 in enumerate(ex.GLUING0):
        for j, A1 in enumerate(ex.GLUING1):
            base_feats.append(branch_features(A0, A1))
            branch_ids.append((i, j))
    base_feats = np.stack(base_feats)

    X, ranks, cids = [], [], []
    profiles = {}
    for cid in ex.EPS_PLUS:
        templates = ex.compile_component(cid)
        rr = []
        for k, (i, j) in enumerate(branch_ids):
            rows = ex.eval_rows(templates, {**ex.GLUING0[i], **ex.GLUING1[j]})
            rr.append(rank_probe(rows, seed=cid * 10_000 + i * 100 + j))
        profiles[cid] = Counter(rr)
        cfeat = scalar_c_features(cid)
        for k, r in enumerate(rr):
            X.append(np.concatenate([base_feats[k], cfeat]))
            ranks.append(float(r))
            cids.append(cid)
    return np.stack(X), np.asarray(ranks, dtype=np.float32), np.asarray(cids), profiles


class PALSoft(nn.Module):
    """One-predicate Complex-Hermitian PAL readout with a graded soft target."""

    def __init__(self, feature_dim: int, d: int = 8, hidden: int = 32, seed: int = 0):
        super().__init__()
        torch.manual_seed(seed)
        self.d = d
        self.enc = nn.Sequential(
            nn.Linear(feature_dim, hidden), nn.ReLU(), nn.Linear(hidden, 2 * d + 1)
        )
        self.c_re = nn.Parameter(torch.randn(d) * 0.3)
        self.c_im = nn.Parameter(torch.randn(d) * 0.3)
        self.alpha = nn.Parameter(torch.tensor(1.0))
        self.beta = nn.Parameter(torch.tensor(0.0))
        self.u = nn.Parameter(torch.tensor(0.0))

    def forward(self, x):
        out = self.enc(x)
        zr, zi, logrho = out[:, : self.d], out[:, self.d : 2 * self.d], out[:, -1]
        rho = F.softplus(logrho) + 1e-3
        re = (self.c_re * zr).sum(-1) + (self.c_im * zi).sum(-1)
        im = (self.c_re * zi).sum(-1) - (self.c_im * zr).sum(-1)
        amp2 = re * re + im * im
        znorm = (zr * zr + zi * zi).sum(-1)
        cnorm = (self.c_re * self.c_re + self.c_im * self.c_im).sum()
        q = (amp2 / (znorm * cnorm + 1e-12)).clamp(1e-4, 1 - 1e-4)
        logit = torch.log(q) - torch.log1p(-q)
        return self.alpha * logit + self.beta + self.u * rho


class RealMLP(nn.Module):
    def __init__(self, feature_dim: int, hidden: int = 32, seed: int = 0):
        super().__init__()
        torch.manual_seed(seed)
        self.net = nn.Sequential(nn.Linear(feature_dim, hidden), nn.ReLU(), nn.Linear(hidden, 1))

    def forward(self, x):
        return self.net(x).squeeze(-1)


def rankdata(a: np.ndarray) -> np.ndarray:
    order = np.argsort(a)
    out = np.empty(len(a), dtype=np.float64)
    i = 0
    while i < len(a):
        j = i + 1
        while j < len(a) and a[order[j]] == a[order[i]]:
            j += 1
        out[order[i:j]] = (i + j - 1) / 2.0
        i = j
    return out


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra, rb = rankdata(a), rankdata(b)
    return float(np.corrcoef(ra, rb)[0, 1])


def metrics(scores: np.ndarray, ranks: np.ndarray) -> dict[str, float]:
    out = {"spearman": spearman(scores, ranks)}
    for k in (20, 50, 100):
        idx = np.argsort(-scores)[:k]
        out[f"top{k}_mean_rank"] = float(ranks[idx].mean())
        out[f"top{k}_rank9_fraction"] = float((ranks[idx] == 9).mean())
    return out


def train_once(cls, Xtr, ytr, Xte, ranks_te, seed: int, steps: int):
    model = cls(Xtr.shape[1], seed=seed)
    opt = torch.optim.Adam(model.parameters(), lr=7e-3)
    xt = torch.tensor(Xtr)
    yt = torch.tensor(ytr)
    for _ in range(steps):
        opt.zero_grad()
        logits = model(xt)
        loss = F.binary_cross_entropy_with_logits(logits, yt)
        loss.backward()
        opt.step()
    with torch.no_grad():
        score = model(torch.tensor(Xte)).cpu().numpy()
    return metrics(score, ranks_te)


def summarize(rows):
    keys = rows[0].keys()
    return {
        k: {"mean": float(np.mean([r[k] for r in rows])), "std": float(np.std([r[k] for r in rows]))}
        for k in keys
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--steps", type=int, default=300)
    args = ap.parse_args()

    X, ranks, cids, profiles = build_dataset()
    soft = np.exp(-(10.0 - ranks) / 2.0).astype(np.float32)
    train = np.asarray([c in TRAIN_COMPONENTS for c in cids])
    test = ~train

    print("teacher rank profiles")
    for cid in ex.EPS_PLUS:
        print(" ", cid, dict(sorted(profiles[cid].items())))
    print("binary exact target positives", 0, "/", len(ranks))
    print("transfer train components", sorted(TRAIN_COMPONENTS))
    print("transfer test components", sorted(TEST_COMPONENTS))
    print("test rank-9 prevalence", float((ranks[test] == 9).mean()))
    print("test mean rank", float(ranks[test].mean()))

    results = {}
    for name, cls in (("PAL-distance", PALSoft), ("MLP-distance", RealMLP)):
        rows = []
        for s in range(args.seeds):
            rows.append(
                train_once(
                    cls,
                    X[train],
                    soft[train],
                    X[test],
                    ranks[test],
                    seed=300 + s,
                    steps=args.steps,
                )
            )
        results[name] = summarize(rows)

    for name, summary in results.items():
        print(name)
        for k, v in summary.items():
            print(f"  {k}: {v['mean']:.6f} +/- {v['std']:.6f}")

    print("NOTE: this is a soft-search experiment only; no learned score enters hard pruning.")


if __name__ == "__main__":
    main()
