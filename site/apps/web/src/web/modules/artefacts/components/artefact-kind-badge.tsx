import { Badge } from "~/web/components/ui/badge";
import { ARTEFACT_KINDS, type ArtefactKind } from "../model/artefact-kind";

// Le type d'un article, en tête de chaque liste et de chaque page : un
// article de recherche et un article de conception ne se lisent pas de la
// même façon, le lecteur doit le savoir avant la première ligne.
export function ArtefactKindBadge({ kind }: { kind: ArtefactKind }) {
  const info = ARTEFACT_KINDS[kind];
  return (
    <Badge tone="accent" color={info.color}>
      {info.label}
    </Badge>
  );
}
