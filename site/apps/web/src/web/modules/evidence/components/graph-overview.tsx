import type { GraphIndex, NodeType } from "~/contracts/evidence";
import { STATUS, STATUS_ORDER } from "../model/status";
import { NodeChip } from "./node-chip";
import { Section } from "./node-bodies";

// Le panneau sans nœud ouvert : la composition du graphe (combien de nœuds
// par statut) et la liste des sources — la porte d'entrée « par le bas ».
export function GraphOverview({
  index,
  onOpen,
}: {
  index: GraphIndex;
  onOpen: (id: string) => void;
}) {
  const counts = new Map<NodeType, number>();
  for (const node of index.byId.values()) counts.set(node.type, (counts.get(node.type) ?? 0) + 1);
  const total = index.byId.size;
  const sources = [...index.byId.values()].filter((node) => node.type === "source");
  return (
    <div className="px-4 pb-6">
      <p className="mt-3 font-sans text-[0.85rem] leading-relaxed text-ink-2">
        Chaque chiffre souligné dans le texte est relié à un nœud de cette chaîne. Cliquez-le, puis
        remontez de dépendance en dépendance jusqu'aux sources.
      </p>
      <Section title={`${total} nœuds`}>
        <div className="flex h-2 w-full overflow-hidden rounded-full bg-paper-2">
          {STATUS_ORDER.map((type) => {
            const count = counts.get(type) ?? 0;
            return count === 0 ? null : (
              <div
                key={type}
                title={`${count} · ${STATUS[type].plural}`}
                style={{ width: `${(count / total) * 100}%`, backgroundColor: STATUS[type].cssVar }}
              />
            );
          })}
        </div>
        <ul className="mt-2 grid grid-cols-2 gap-x-3 gap-y-1 font-sans text-[0.78rem]">
          {STATUS_ORDER.map((type) => {
            const count = counts.get(type) ?? 0;
            return count === 0 ? null : (
              <li key={type} className="flex items-center gap-1.5">
                <span
                  aria-hidden
                  className="size-2 rounded-full"
                  style={{ backgroundColor: STATUS[type].cssVar }}
                />
                <span className="tabular-nums text-ink">{count}</span>
                <span className="text-ink-2">
                  {count === 1 ? STATUS[type].label : STATUS[type].plural}
                </span>
              </li>
            );
          })}
        </ul>
      </Section>
      <Section title={sources.length === 1 ? "Source" : `${sources.length} sources`}>
        <ul className="space-y-1">
          {sources.map((node) => (
            <li key={node.id}>
              <NodeChip node={node} onOpen={onOpen} />
            </li>
          ))}
        </ul>
      </Section>
    </div>
  );
}
