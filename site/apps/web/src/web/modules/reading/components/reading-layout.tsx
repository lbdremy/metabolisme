import { Link } from "@tanstack/react-router";
import { GitBranch, PanelRightClose, PanelRightOpen } from "lucide-react";
import { useState, type ReactNode } from "react";
import type { PublicationRef } from "~/content-assets/public";
import { Wordmark } from "~/web/components/ui/logo";
import { cn } from "~/web/lib/cn";
import { EvidencePanel } from "~/web/modules/evidence/components/evidence-panel";
import { useEvidenceExplorerViewModel } from "~/web/modules/evidence/use-evidence-explorer-view-model";
import { MarkdownDocument } from "./markdown-document";

// La page de lecture : deux tiers de texte, un tiers de chaîne de preuves.
// Sur un petit écran, le panneau se replie et s'ouvre par-dessus le texte
// (ouvrir un nœud l'ouvre). À monter avec une `key` par publication.
export function ReadingLayout({
  publication,
  header,
  markdown,
  selectedId,
  onNavigate,
  footer,
  robotsNoIndex = false,
}: {
  publication: PublicationRef;
  header: ReactNode;
  markdown: string;
  selectedId: string | null;
  onNavigate: (id: string | null) => void;
  footer?: ReactNode;
  robotsNoIndex?: boolean;
}) {
  const vm = useEvidenceExplorerViewModel({ publication, selectedId, onNavigate });
  // Ouverture du panneau sur petit écran : état d'interface local, pas métier.
  const [panelOpen, setPanelOpen] = useState(false);
  const panelVisible = panelOpen || selectedId !== null;
  const ready = vm.graphStatus === "ready";

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-30 flex h-12 shrink-0 items-center gap-4 border-b border-rule bg-paper/95 px-4 backdrop-blur sm:px-6">
        <Link to="/" className="shrink-0">
          <Wordmark />
        </Link>
        <nav className="ml-auto flex items-center gap-2 font-sans text-[0.8rem]">
          {robotsNoIndex && (
            <span className="hidden rounded-full border border-rule px-2 py-0.5 text-ink-3 sm:inline">
              note partagée par lien
            </span>
          )}
          <button
            type="button"
            onClick={() => setPanelOpen((open) => !open)}
            className="inline-flex items-center gap-1.5 rounded-md border border-rule px-2 py-1 text-ink-2 hover:bg-paper-2 lg:hidden"
          >
            {panelVisible ? (
              <PanelRightClose aria-hidden className="size-4" />
            ) : (
              <PanelRightOpen aria-hidden className="size-4" />
            )}
            Preuves
          </button>
          <span className="hidden items-center gap-1.5 text-ink-3 lg:inline-flex">
            <GitBranch aria-hidden className="size-3.5" />
            chaîne de preuves
          </span>
        </nav>
      </header>

      <div className="flex min-h-0 grow">
        <main className="min-w-0 grow px-5 py-8 sm:px-8 lg:w-2/3 lg:px-12">
          <div className="mx-auto max-w-[68ch]">
            {header}
            <div className="mt-8">
              <MarkdownDocument
                markdown={markdown}
                isKnown={vm.isKnown}
                ready={ready}
                activeId={selectedId}
                onOpen={(id) => {
                  setPanelOpen(true);
                  vm.onOpen(id);
                }}
              />
            </div>
            {footer !== undefined && (
              <div className="mt-12 border-t border-rule pt-6">{footer}</div>
            )}
          </div>
        </main>

        <aside
          className={cn(
            "fixed inset-x-0 bottom-0 top-12 z-20 border-l border-rule bg-paper-2 transition-transform lg:sticky lg:top-12 lg:h-[calc(100vh-3rem)] lg:w-1/3 lg:max-w-[34rem] lg:translate-x-0 lg:shrink-0",
            panelVisible ? "translate-x-0" : "translate-x-full",
          )}
        >
          <EvidencePanel
            vm={{
              ...vm,
              onClose: () => {
                setPanelOpen(false);
                vm.onClose();
              },
            }}
            publication={publication}
          />
        </aside>
      </div>
    </div>
  );
}
