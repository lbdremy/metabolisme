import type { EvidenceGraph, EvidenceNode, NodeType } from "./graph.ts";

// Index pur d'un graphe de preuves : accès par identifiant, relations
// inverses (« qui dépend de ce nœud ? »), remontée de la chaîne jusqu'aux
// sources. Aucune I/O — testable table par table.

export type GraphIndex = {
  readonly byId: ReadonlyMap<string, EvidenceNode>;
  // Pour chaque nœud, les nœuds qui le citent dans depends_on.
  readonly dependents: ReadonlyMap<string, ReadonlyArray<string>>;
  // Pour chaque limite, les nœuds qui la déclarent dans limitations.
  readonly limitedNodes: ReadonlyMap<string, ReadonlyArray<string>>;
  readonly order: ReadonlyArray<string>;
};

export function indexGraph(graph: EvidenceGraph): GraphIndex {
  const byId = new Map<string, EvidenceNode>();
  const dependents = new Map<string, string[]>();
  const limitedNodes = new Map<string, string[]>();
  for (const node of graph.nodes) {
    byId.set(node.id, node);
  }
  for (const node of graph.nodes) {
    for (const dep of node.depends_on) {
      const list = dependents.get(dep) ?? [];
      list.push(node.id);
      dependents.set(dep, list);
    }
    for (const limit of node.limitations) {
      const list = limitedNodes.get(limit) ?? [];
      list.push(node.id);
      limitedNodes.set(limit, list);
    }
  }
  return {
    byId,
    dependents,
    limitedNodes,
    order: graph.nodes.map((node) => node.id),
  };
}

// Références non résolues : un depends_on / limitations qui ne pointe sur
// aucun nœud. Un graphe publié doit en être exempt (rule INTRO §21 n°13).
export function danglingReferences(graph: EvidenceGraph): { from: string; to: string }[] {
  const ids = new Set(graph.nodes.map((node) => node.id));
  const dangling: { from: string; to: string }[] = [];
  for (const node of graph.nodes) {
    for (const to of [...node.depends_on, ...node.limitations]) {
      if (!ids.has(to)) dangling.push({ from: node.id, to });
    }
    if (node.type === "hypothesis") {
      for (const to of node.affects) {
        if (!ids.has(to)) dangling.push({ from: node.id, to });
      }
    }
  }
  return dangling;
}

export type ChainStep = {
  readonly id: string;
  readonly depth: number;
};

// La chaîne amont d'un nœud : ses dépendances, puis les leurs, en largeur,
// chaque nœud une seule fois (à sa profondeur minimale). C'est ce que le
// panneau « dépile » jusqu'aux sources.
export function upstreamChain(index: GraphIndex, rootId: string): ChainStep[] {
  const seen = new Set<string>([rootId]);
  const queue: ChainStep[] = [{ id: rootId, depth: 0 }];
  const out: ChainStep[] = [];
  while (queue.length > 0) {
    const step = queue.shift();
    if (step === undefined) break;
    const node = index.byId.get(step.id);
    if (node === undefined) continue;
    if (step.depth > 0) out.push(step);
    for (const dep of node.depends_on) {
      if (seen.has(dep)) continue;
      seen.add(dep);
      queue.push({ id: dep, depth: step.depth + 1 });
    }
  }
  return out;
}

// Les sources (S-xx) qui, directement ou non, soutiennent un nœud.
export function upstreamSources(index: GraphIndex, rootId: string): string[] {
  return upstreamChain(index, rootId)
    .map((step) => step.id)
    .filter((id) => index.byId.get(id)?.type === "source");
}

export function groupByType(
  index: GraphIndex,
  ids: ReadonlyArray<string>,
): Partial<Record<NodeType, EvidenceNode[]>> {
  const groups: Partial<Record<NodeType, EvidenceNode[]>> = {};
  for (const id of ids) {
    const node = index.byId.get(id);
    if (node === undefined) continue;
    (groups[node.type] ??= []).push(node);
  }
  return groups;
}
