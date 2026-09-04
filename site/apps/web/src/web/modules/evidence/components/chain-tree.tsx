import type { ChainStep, GraphIndex } from "~/contracts/evidence";
import { STATUS } from "../model/status";

// Toute la chaîne amont d'un nœud, jusqu'aux sources, par profondeur :
// c'est la vue « dépiler ». Chaque ligne est cliquable.
export function ChainTree({
  index,
  chain,
  onOpen,
}: {
  index: GraphIndex;
  chain: ReadonlyArray<ChainStep>;
  onOpen: (id: string) => void;
}) {
  if (chain.length === 0) {
    return (
      <p className="font-sans text-[0.8rem] text-ink-3">
        Ce nœud ne dépend de rien : c'est un point de départ.
      </p>
    );
  }
  const maxDepth = Math.max(...chain.map((step) => step.depth));
  return (
    <ol className="space-y-0.5 font-sans text-[0.8rem]">
      {chain.map((step) => {
        const node = index.byId.get(step.id);
        if (node === undefined) return null;
        const status = STATUS[node.type];
        return (
          <li key={step.id} style={{ paddingLeft: `${(step.depth - 1) * 0.9}rem` }}>
            <button
              type="button"
              onClick={() => onOpen(step.id)}
              className="flex w-full items-baseline gap-2 rounded px-1.5 py-0.5 text-left hover:bg-white"
            >
              <span
                className="shrink-0 rounded px-1 font-mono text-[0.66rem] font-semibold text-white"
                style={{ backgroundColor: status.cssVar }}
              >
                {node.id}
              </span>
              <span className="line-clamp-1 text-ink-2">{node.title}</span>
              {step.depth === maxDepth && node.type === "source" && (
                <span className="ml-auto shrink-0 text-[0.66rem] uppercase tracking-wider text-ink-3">
                  origine
                </span>
              )}
            </button>
          </li>
        );
      })}
    </ol>
  );
}
