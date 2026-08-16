"""Minimal proof-DAG skeleton for adjacent Levin--Wen plaquette commutation.

This experiment does *not* re-prove categorical coherence from F-symbol
polynomials.  It machine-encodes the classical graphical proof from
Levin--Wen Appendix C:

1. B_p^s is represented on the fattened lattice by inserting an s-loop around p.
2. Inserting loops around two adjacent plaquettes is order-independent as a
   decorated graphical state.
3. The coherent reduction map from fattened diagrams to the physical lattice is
   independent of the chosen local-rule reduction history.

Thus the two operator schedules have a common intermediate diagram.  The
result is a constant-size diamond certificate.

Research labels:
- CLASSICAL: the graphical proof and coherent reduction.
- REFORMULATION: representing it as an explicit operation-history proof DAG.
- NEGATIVE BENCHMARK: the constant-size certificate is not AEG-specific; it is
  already the classical string-net graphical argument.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet, Iterable, List, Tuple


@dataclass(frozen=True, order=True)
class Loop:
    face: str
    label: str


@dataclass(frozen=True)
class FattenedDiagram:
    """Only the data relevant to the commutation certificate.

    `base_state` is intentionally opaque: the proof works uniformly for every
    admissible string-net state.  Inserted loops are recorded as an unordered
    multiset-like set because the graphical state depends on which loops are
    present, not on the temporal order in which they were inserted.
    """

    base_state: str
    loops: FrozenSet[Loop] = frozenset()

    def insert(self, face: str, label: str) -> "FattenedDiagram":
        loop = Loop(face, label)
        if loop in self.loops:
            raise ValueError("this tiny certificate model expects distinct face/label insertions")
        return FattenedDiagram(self.base_state, self.loops | {loop})


@dataclass(frozen=True)
class ProofNode:
    id: str
    kind: str
    payload: str


@dataclass(frozen=True)
class ProofEdge:
    source: str
    target: str
    lemma: str


@dataclass
class ProofDAG:
    nodes: Dict[str, ProofNode]
    edges: List[ProofEdge]

    def add_node(self, node: ProofNode) -> None:
        if node.id in self.nodes:
            raise ValueError(node.id)
        self.nodes[node.id] = node

    def add_edge(self, source: str, target: str, lemma: str) -> None:
        assert source in self.nodes and target in self.nodes
        self.edges.append(ProofEdge(source, target, lemma))

    def trusted_lemmas(self) -> Tuple[str, ...]:
        return tuple(sorted({edge.lemma for edge in self.edges}))


def insertion_order_independent(
    state: FattenedDiagram,
    left_face: str,
    right_face: str,
    left_label: str,
    right_label: str,
) -> bool:
    lr = state.insert(right_face, right_label).insert(left_face, left_label)
    rl = state.insert(left_face, left_label).insert(right_face, right_label)
    return lr == rl


def build_adjacent_commutation_certificate(
    left_face: str = "L",
    right_face: str = "R",
    left_label: str = "tau",
    right_label: str = "tau",
) -> Tuple[ProofDAG, FattenedDiagram]:
    """Build the constant-size diamond certificate.

    Trusted lemma boundary:
    - graphical_semantics: B_p^s equals coherent reduction after loop insertion;
    - coherent_reduction: the fattened diagram has a well-defined physical
      reduction independent of local-rule evaluation order.

    The middle equality itself is structural and checked directly here.
    """

    x = FattenedDiagram("arbitrary-admissible-state")
    after_r = x.insert(right_face, right_label)
    after_l = x.insert(left_face, left_label)
    middle_lr = after_r.insert(left_face, left_label)
    middle_rl = after_l.insert(right_face, right_label)
    assert middle_lr == middle_rl

    dag = ProofDAG(nodes={}, edges=[])
    for node in (
        ProofNode("LR", "operator-history", "B_L B_R |X>"),
        ProofNode("after-R", "fattened-diagram", repr(after_r)),
        ProofNode("after-L", "fattened-diagram", repr(after_l)),
        ProofNode("join", "fattened-diagram", repr(middle_lr)),
        ProofNode("RL", "operator-history", "B_R B_L |X>"),
    ):
        dag.add_node(node)

    # Read the left branch from LR to the common two-loop diagram.
    dag.add_edge("LR", "after-R", "graphical_semantics")
    dag.add_edge("after-R", "join", "loop_insertion")

    # Read the right branch backwards from RL to the same common diagram.
    dag.add_edge("RL", "after-L", "graphical_semantics")
    dag.add_edge("after-L", "join", "loop_insertion")

    # The semantic conclusion uses one shared coherent reduction of `join`.
    # We record it as metadata/trusted boundary instead of inventing a new node
    # for every physical output basis state.
    return dag, middle_lr


def certificate_metrics(dag: ProofDAG) -> Dict[str, object]:
    return {
        "proof_nodes": len(dag.nodes),
        "proof_edges": len(dag.edges),
        "trusted_lemmas": dag.trusted_lemmas() + ("coherent_reduction",),
        "arithmetic_operations": 0,
        "depends_on_hilbert_dimension": False,
    }


def direct_max_sector_metrics() -> Dict[str, int]:
    """Frozen from the independently verified adjacent-plaquette baseline."""
    return {
        "hilbert_dimension": 170,
        "left_operator_nnz": 1551,
        "right_operator_nnz": 1551,
        "product_nnz": 11922,
        "scalar_multiplies_per_order": 14854,
    }


def main() -> None:
    state = FattenedDiagram("X")
    assert insertion_order_independent(state, "L", "R", "tau", "tau")

    dag, join = build_adjacent_commutation_certificate()
    assert join.loops == frozenset({Loop("L", "tau"), Loop("R", "tau")})

    print("certificate")
    for key, value in certificate_metrics(dag).items():
        print(f"  {key}: {value}")

    print("direct instantiated max-sector baseline")
    for key, value in direct_max_sector_metrics().items():
        print(f"  {key}: {value}")

    print("verdict")
    print("  The structural certificate is constant-size, but it is the classical")
    print("  Levin-Wen graphical proof encoded as an explicit history DAG.")
    print("  No AEG-specific proof compression is established.")


if __name__ == "__main__":
    main()
