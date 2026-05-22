"""Lightweight causal DAG helper.

Stores nodes (variables) and directed edges (assumed causal relationships)
without depending on networkx so that the package's core install footprint
remains minimal. If networkx is available the helper can export the DAG to
a :class:`networkx.DiGraph` for visualisation via :func:`to_networkx`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Set, Tuple


@dataclass
class DietDAG:
    """A directed acyclic graph encoding assumed causal relationships."""

    nodes: Set[str] = field(default_factory=set)
    edges: Set[Tuple[str, str]] = field(default_factory=set)
    edge_labels: Dict[Tuple[str, str], str] = field(default_factory=dict)

    def add_node(self, name: str) -> "DietDAG":
        self.nodes.add(name)
        return self

    def add_edge(self, parent: str, child: str, label: str = "") -> "DietDAG":
        self.nodes.update({parent, child})
        self.edges.add((parent, child))
        if label:
            self.edge_labels[(parent, child)] = label
        return self

    def parents(self, node: str) -> List[str]:
        return [p for p, c in self.edges if c == node]

    def children(self, node: str) -> List[str]:
        return [c for p, c in self.edges if p == node]

    def ancestors(self, node: str) -> Set[str]:
        seen: Set[str] = set()
        stack = list(self.parents(node))
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(self.parents(cur))
        return seen

    def descendants(self, node: str) -> Set[str]:
        seen: Set[str] = set()
        stack = list(self.children(node))
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(self.children(cur))
        return seen

    def is_acyclic(self) -> bool:
        # Kahn's algorithm.
        in_degree = {n: 0 for n in self.nodes}
        for _, c in self.edges:
            in_degree[c] = in_degree.get(c, 0) + 1
        queue = [n for n, d in in_degree.items() if d == 0]
        visited = 0
        while queue:
            n = queue.pop()
            visited += 1
            for c in self.children(n):
                in_degree[c] -= 1
                if in_degree[c] == 0:
                    queue.append(c)
        return visited == len(self.nodes)

    def to_mermaid(self) -> str:
        """Return a Mermaid flowchart representation."""
        lines = ["flowchart LR"]
        for n in sorted(self.nodes):
            lines.append(f"    {n.replace(' ', '_')}[{n}]")
        for (p, c), label in {(e, self.edge_labels.get(e, "")) for e in self.edges}:
            arrow = f"-- {label} -->" if label else "-->"
            lines.append(f"    {p.replace(' ', '_')} {arrow} {c.replace(' ', '_')}")
        return "\n".join(lines)

    def to_networkx(self):  # type: ignore[override]
        try:
            import networkx as nx
        except ImportError as exc:
            raise ImportError(
                "networkx is required for to_networkx(); install with "
                "`pip install networkx`."
            ) from exc
        g = nx.DiGraph()
        g.add_nodes_from(self.nodes)
        for (p, c) in self.edges:
            label = self.edge_labels.get((p, c), "")
            g.add_edge(p, c, label=label)
        return g


def default_diet_dag() -> DietDAG:
    """A small example DAG for didactic purposes."""
    dag = DietDAG()
    (
        dag.add_edge("age", "bmi")
        .add_edge("sex", "bmi")
        .add_edge("bmi", "type_2_diabetes")
        .add_edge("bmi", "hypertension")
        .add_edge("diet", "bmi", label="energy_balance")
        .add_edge("diet", "ldl_mg_dl", label="saturated_fat")
        .add_edge("diet", "systolic_bp_mmhg", label="sodium")
        .add_edge("type_2_diabetes", "hba1c_pct")
        .add_edge("activity", "bmi")
        .add_edge("activity", "diet")
    )
    return dag
