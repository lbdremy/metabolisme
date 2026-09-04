import { ArrowLeft, ChevronRight, X } from "lucide-react";
import type { PublicationRef } from "~/content-assets/public";
import type { EvidenceFile, EvidenceNode } from "~/contracts/evidence";
import { IconButton } from "~/web/components/ui/icon-button";
import type { EvidenceExplorerViewModel } from "../model/evidence-explorer-model";
import { STATUS } from "../model/status";
import { ChainTree } from "./chain-tree";
import { FileViewer } from "./file-viewer";
import { GraphOverview } from "./graph-overview";
import {
  ComputedBody,
  DefinitionBody,
  HypothesisBody,
  ObservationBody,
  Section,
  SourceBody,
} from "./node-bodies";
import { RelationGroups } from "./relations";
import { StatusBadge } from "./status-badge";

// Le panneau d'exploration : un nœud à la fois, son statut, son corps, ses
// relations (ce dont il dépend, ce qui en dépend, ses limites) et toute sa
// chaîne amont. Un fil de navigation permet de revenir. Composant de
// présentation : les décisions viennent du ViewModel.

type PanelViewModel = EvidenceExplorerViewModel & {
  onOpen: (id: string) => void;
  onBack: () => void;
  onClose: () => void;
};

function sourceFilesOf(vm: PanelViewModel, node: EvidenceNode): EvidenceFile[] {
  if (vm.index === null) return [];
  return node.depends_on.flatMap((dep) => {
    const source = vm.index?.byId.get(dep);
    return source?.type === "source" ? source.files : [];
  });
}

function originalUrlOf(vm: PanelViewModel, nodeId: string): string | null {
  const node = vm.index?.byId.get(nodeId);
  return node?.type === "source" ? node.source_url : null;
}

export function EvidencePanel({
  vm,
  publication,
}: {
  vm: PanelViewModel;
  publication: PublicationRef;
}) {
  const { selected, index } = vm;

  return (
    <div className="flex h-full min-h-0 flex-col bg-paper-2/60">
      <header className="flex h-11 shrink-0 items-center gap-1 border-b border-rule px-2">
        {selected !== null && (
          <IconButton
            icon={ArrowLeft}
            label="Nœud précédent"
            onClick={vm.onBack}
            disabled={!vm.canGoBack}
          />
        )}
        <span className="min-w-0 grow truncate px-1 font-sans text-[0.8rem] font-semibold text-ink">
          {selected === null ? "Chaîne de preuves" : selected.id}
        </span>
        {selected !== null && <IconButton icon={X} label="Fermer le nœud" onClick={vm.onClose} />}
      </header>

      {vm.trail.length > 1 && vm.openFile === null && (
        <nav
          aria-label="Fil de navigation"
          className="flex shrink-0 items-center gap-0.5 overflow-x-auto border-b border-rule px-2 py-1.5 font-mono text-[0.68rem]"
        >
          {vm.trail.map((node, i) => (
            <span key={node.id} className="flex shrink-0 items-center gap-0.5">
              {i > 0 && <ChevronRight aria-hidden className="size-3 text-ink-3" />}
              <button
                type="button"
                onClick={() => vm.onOpen(node.id)}
                aria-current={i === vm.trail.length - 1 || undefined}
                className="rounded px-1 py-px text-ink-3 hover:bg-white hover:text-ink aria-[current]:text-ink"
                style={i === vm.trail.length - 1 ? { color: STATUS[node.type].cssVar } : undefined}
              >
                {node.id}
              </button>
            </span>
          ))}
        </nav>
      )}

      {vm.graphStatus === "error" ? (
        <p className="p-4 font-sans text-sm text-status-interpretation">{vm.errorMessage}</p>
      ) : index === null ? (
        <p className="p-4 font-sans text-sm text-ink-3">Chargement de la chaîne de preuves…</p>
      ) : vm.openFile !== null ? (
        <FileViewer
          publication={publication}
          file={vm.openFile.file}
          page={vm.openFile.page}
          originalUrl={originalUrlOf(vm, vm.openFile.nodeId)}
          language={
            vm.openFile.file.path.endsWith(".py")
              ? "python"
              : vm.openFile.file.path.endsWith(".json")
                ? "json"
                : null
          }
          onBack={vm.onCloseFile}
        />
      ) : selected === null ? (
        vm.selectedMissing ? (
          <p className="p-4 font-sans text-sm text-ink-2">
            Ce nœud n'existe pas dans cette chaîne de preuves.
          </p>
        ) : (
          <div className="min-h-0 grow overflow-y-auto">
            <GraphOverview index={index} onOpen={vm.onOpen} />
          </div>
        )
      ) : (
        <div className="min-h-0 grow overflow-y-auto px-4 pb-8">
          <div className="mt-3 flex items-center gap-2">
            <StatusBadge type={selected.type} />
          </div>
          <h2 className="mt-2 font-serif text-[1rem] leading-snug text-ink">{selected.title}</h2>
          {selected.notes !== undefined && (
            <p className="mt-2 font-sans text-[0.78rem] leading-relaxed text-ink-2">
              {selected.notes}
            </p>
          )}

          <NodeBody vm={vm} node={selected} />

          <Section title="Repose sur">
            <RelationGroups
              index={index}
              ids={selected.depends_on}
              onOpen={vm.onOpen}
              emptyLabel={
                selected.type === "source"
                  ? "Une source est un point de départ : elle ne dépend de rien dans la chaîne."
                  : "Ce nœud ne déclare aucune dépendance."
              }
            />
          </Section>

          {selected.limitations.length > 0 && (
            <Section title="Limites déclarées">
              <RelationGroups index={index} ids={selected.limitations} onOpen={vm.onOpen} />
            </Section>
          )}

          {selected.type === "hypothesis" && selected.affects.length > 0 && (
            <Section title="Affecte">
              <RelationGroups index={index} ids={selected.affects} onOpen={vm.onOpen} />
            </Section>
          )}

          {(index.dependents.get(selected.id)?.length ?? 0) > 0 && (
            <Section title="Utilisé par">
              <RelationGroups
                index={index}
                ids={index.dependents.get(selected.id) ?? []}
                onOpen={vm.onOpen}
              />
            </Section>
          )}

          {selected.type === "limit" && (index.limitedNodes.get(selected.id)?.length ?? 0) > 0 && (
            <Section title="Limite de">
              <RelationGroups
                index={index}
                ids={index.limitedNodes.get(selected.id) ?? []}
                onOpen={vm.onOpen}
              />
            </Section>
          )}

          {vm.chain.length > 0 && (
            <Section title="Toute la chaîne, jusqu'aux sources">
              <ChainTree index={index} chain={vm.chain} onOpen={vm.onOpen} />
            </Section>
          )}
        </div>
      )}
    </div>
  );
}

function NodeBody({ vm, node }: { vm: PanelViewModel; node: EvidenceNode }) {
  const onOpenFile = (file: EvidenceFile, page: number | null) =>
    vm.onOpenFile(node.id, file, page);
  switch (node.type) {
    case "source":
      return <SourceBody node={node} onOpenFile={onOpenFile} />;
    case "definition":
      return <DefinitionBody node={node} />;
    case "hypothesis":
      return <HypothesisBody node={node} />;
    case "observation":
      return (
        <ObservationBody
          node={node}
          sourceFiles={sourceFilesOf(vm, node)}
          onOpenFile={onOpenFile}
        />
      );
    case "transformation":
    case "measure":
    case "result":
      return <ComputedBody node={node} onOpenFile={onOpenFile} />;
    case "interpretation":
    case "value":
    case "choice":
    case "proposal":
    case "limit":
      return null;
  }
}
