import { Eye } from "lucide-react";
import { Badge } from "~/web/components/ui/badge";

// Marque un post encore en attente de relecture : absent de l'index (sauf
// mode relecture), mais lisible à son adresse. Le lecteur doit savoir que ce
// texte n'a pas encore été relu.
export function InReviewBadge() {
  return (
    <Badge tone="outline" color="var(--color-status-limit)">
      <Eye aria-hidden className="size-3" />
      En attente de relecture
    </Badge>
  );
}
