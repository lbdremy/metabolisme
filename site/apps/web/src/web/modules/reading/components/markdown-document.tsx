import { useMemo } from "react";
import Markdown, { defaultUrlTransform } from "react-markdown";
import remarkGfm from "remark-gfm";
import { parseEvidenceHref } from "~/contracts/evidence";
import { EvidenceAnchor } from "~/web/modules/evidence/components/evidence-anchor";
import { remarkEvidenceIds } from "../model/remark-evidence-ids";

// Le texte (article ou note) rendu depuis Markdown. Deux sortes de liens :
// les ancres de preuve (ev:…) deviennent des boutons qui ouvrent le panneau,
// les autres restent des liens ordinaires ouverts dans un nouvel onglet.
export function MarkdownDocument({
  markdown,
  isKnown,
  ready,
  activeId,
  onOpen,
}: {
  markdown: string;
  isKnown: (id: string) => boolean;
  ready: boolean;
  activeId: string | null;
  onOpen: (id: string) => void;
}) {
  const remarkPlugins = useMemo(
    () => [remarkGfm, [remarkEvidenceIds, { known: isKnown }] as const],
    [isKnown],
  );
  return (
    <div className="prose-reading">
      <Markdown
        remarkPlugins={remarkPlugins as never}
        urlTransform={(url) => (parseEvidenceHref(url) !== null ? url : defaultUrlTransform(url))}
        components={{
          a({ href, children }) {
            const id = parseEvidenceHref(href);
            if (id !== null) {
              return (
                <EvidenceAnchor id={id} active={id === activeId} ready={ready} onOpen={onOpen}>
                  {children}
                </EvidenceAnchor>
              );
            }
            return (
              <a href={href} target="_blank" rel="noopener noreferrer">
                {children}
              </a>
            );
          },
        }}
      >
        {markdown}
      </Markdown>
    </div>
  );
}
