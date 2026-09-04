import type { EvidenceNode, GraphIndex, NodeType } from "~/contracts/evidence";
import { groupByType } from "~/contracts/evidence";
import { STATUS, STATUS_ORDER } from "../model/status";
import { NodeChip } from "./node-chip";

// Les relations d'un nœud, groupées par statut dans l'ordre de la chaîne.
export function RelationGroups({
  index,
  ids,
  onOpen,
  emptyLabel,
}: {
  index: GraphIndex;
  ids: ReadonlyArray<string>;
  onOpen: (id: string) => void;
  emptyLabel?: string;
}) {
  const groups = groupByType(index, ids);
  const present = STATUS_ORDER.filter((type) => (groups[type]?.length ?? 0) > 0);
  if (present.length === 0) {
    return emptyLabel === undefined ? null : (
      <p className="font-sans text-[0.8rem] text-ink-3">{emptyLabel}</p>
    );
  }
  return (
    <div className="space-y-3">
      {present.map((type) => (
        <RelationGroup key={type} type={type} nodes={groups[type] ?? []} onOpen={onOpen} />
      ))}
    </div>
  );
}

function RelationGroup({
  type,
  nodes,
  onOpen,
}: {
  type: NodeType;
  nodes: ReadonlyArray<EvidenceNode>;
  onOpen: (id: string) => void;
}) {
  const status = STATUS[type];
  return (
    <div>
      <div className="mb-1 flex items-center gap-1.5 font-sans text-[0.68rem] font-semibold uppercase tracking-wider text-ink-3">
        <span
          aria-hidden
          className="size-1.5 rounded-full"
          style={{ backgroundColor: status.cssVar }}
        />
        {nodes.length === 1 ? status.label : status.plural}
      </div>
      <ul className="space-y-1">
        {nodes.map((node) => (
          <li key={node.id}>
            <NodeChip node={node} onOpen={onOpen} />
          </li>
        ))}
      </ul>
    </div>
  );
}
