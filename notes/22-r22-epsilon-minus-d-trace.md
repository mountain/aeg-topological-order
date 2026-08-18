# R(2,2) fresh epsilon-minus D chirality localization

**Status:** `CANDIDATE-NEW / EXACT CANONICAL REPLAY / Phase 1 complete`

This note replaces the chirality-localization portion of the superseded epsilon-minus closure with a fresh replay from the full-`C*` canonical scalar representatives.

## 1. Scope

The independently local-F-obstructed epsilon-minus scalar components are

\[
4,6,12,14.
\]

The deep canonical verification frontier is

\[
\boxed{5,7,13,15}.
\]

For each of these four scalar components the experiment

- `experiments/r22_epsminus_d_trace.py`

replays all

\[
2^8=256
\]

local Clifford chirality assignments directly from the multiplicity-aware D-layer pentagons.

The implementation:

1. installs the 24 Pauli/Clifford stabilizer seeds;
2. computes the 48 cross-D projective intertwiner shapes exactly;
3. associates a required nonzero amplitude `t_j` to every projective cross-D block;
4. substitutes this data into every complete D-layer pentagon;
5. rejects a branch when a single nonzero amplitude monomial is forced to vanish;
6. otherwise rejects a branch when two pentagon entries impose different exact phases on the same amplitude-monomial ratio.

No finite-field, numerical, or learned result is used in this classification.

## 2. Exact result

A clean GitHub Actions replay gives, for **each** of scalar components

\[
5,7,13,15,
\]

the identical count

\[
\boxed{
256
\longrightarrow
64
\longrightarrow
4.
}
\]

More explicitly,

\[
\boxed{
192\text{ structural contradictions},
\qquad
60\text{ exact phase conflicts},
\qquad
4\text{ survivors}.
}
\]

The survivor masks are in every case

\[
\boxed{0,105,150,255}.
\]

These are exactly the four assignments for which chirality is constant on each of the two size-four `Y`-parity transport orbits.

## 3. Compact structural certificate

The first structural failure (mask `1` in the frozen bit convention) occurs at

\[
(g,X,g,X;X)_{00}.
\]

After the exact projective-D substitution the entry contains a single nonzero amplitude monomial with coefficient `1`.  The amplitudes are required nonzero for invertible D transport, so this is an immediate contradiction.

In the frozen cross-D ordering the example monomial is `t_24 t_34`, but the index numbers are implementation metadata; the pentagon provenance is the invariant certificate.

## 4. Compact phase-conflict certificate

The first non-structural failure (mask `6`) reaches the amplitude-ratio stage.  Two local pentagon entries constrain the same ratio of D amplitudes:

\[
(g,h,X,X;X)_{11}:\qquad R=-1,
\]

while

\[
(h,g,X,X;X)_{00}:\qquad R=+1.
\]

Thus the same nonzero monomial ratio is required to equal both signs, an exact contradiction.

In the frozen implementation the ratio is `t_32/t_40`; again the amplitude indices are bookkeeping, while the pair of pentagon entries is the compact proof provenance.

## 5. Agreement with the PAL/PCRG relation geometry

The auxiliary experiment

- `experiments/r22_pal_edge_geometry.py`

lifts the chirality field on each parity `K_4` to edge relations

\[
\eta_{uv}=c_uc_v
\]

and computes normalized projective overlap with the coherent edge predicate.

For all 256 chirality masks it gives

\[
Q=0\text{ on }192,
\qquad
Q=1/9\text{ on }60,
\qquad
Q=1\text{ on }4,
\]

with the `Q=1` masks again

\[
0,105,150,255.
\]

The clean exact pentagon replay now shows that this projective relation-space stratification agrees with the actual D verifier hierarchy on all four deep-frontier scalar components:

\[
\boxed{
Q=0\leftrightarrow\text{structural failure},
\quad
Q=1/9\leftrightarrow\text{phase failure},
\quad
Q=1\leftrightarrow\text{D survivor}.
}
\]

This agreement is an exact empirical identification for the present D subproblem.  It does not make the PAL geometry part of the proof: the pentagon certificates remain authoritative.

## 6. Compute result

The initial exact implementation required roughly five minutes for one 256-mask replay because it rebuilt the same 4-variable projective nullspaces repeatedly.

Caching each cross-D projective shape by the local chirality signature actually read by its singleton pentagons reduces a complete 256-mask component replay to roughly ten seconds on the clean Actions runner, while reproducing the same counts, survivor set, and local certificates.

This is a representation/compilation improvement, not a mathematical pruning change.

## 7. Phase gate

Phase 1 of `notes/21-r22-complete-research-schedule.md` is now complete.

The exact search entering Phase 2 contains at most

\[
\boxed{
4\text{ scalar components}
\times
4\text{ orbit-level chirality masks}
=
16\text{ branches}.
}
\]

The next task is exact D-amplitude closure on these 16 branches, followed by characteristic-zero substitution into every D-layer pentagon.
