import type { Link, Root, Text } from "mdast";
import { visit } from "unist-util-visit";
import { evidenceHref, splitBareIds } from "~/contracts/evidence";

// Plugin remark : un identifiant nu dans le texte (« (R-07) ») devient un
// lien « ev:R-07 », s'il existe dans le graphe. Les textes déjà dans un lien
// ne sont pas touchés. Pure transformation d'arbre.
export function remarkEvidenceIds(options: { known: (id: string) => boolean }) {
  return (tree: Root) => {
    visit(tree, "text", (node: Text, index, parent) => {
      if (parent === undefined || index === undefined || parent.type === "link") return;
      const segments = splitBareIds(node.value, options.known);
      if (segments.length === 1 && segments[0]?.kind === "text") return;
      const replacement: (Text | Link)[] = segments.map((segment) =>
        segment.kind === "text"
          ? { type: "text", value: segment.text }
          : {
              type: "link",
              url: evidenceHref(segment.id),
              children: [{ type: "text", value: segment.id }],
            },
      );
      parent.children.splice(index, 1, ...replacement);
      return index + replacement.length;
    });
  };
}
