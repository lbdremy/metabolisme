import { useEffect, useState, useSyncExternalStore } from "react";
import { fetchGraph, type PublicationRef } from "~/content-assets/public";
import {
  createEvidenceExplorerModel,
  type EvidenceExplorerViewModel,
} from "./model/evidence-explorer-model";

// Hook ViewModel : câblage React uniquement. Le nœud ouvert vient de l'URL
// (validé par la route) ; la navigation est un callback fourni par la route.
// Le composant qui l'utilise doit être re-monté (key) quand la publication
// change — le modèle est créé une fois pour la durée du montage.
export function useEvidenceExplorerViewModel(args: {
  publication: PublicationRef;
  selectedId: string | null;
  onNavigate: (id: string | null) => void;
}): EvidenceExplorerViewModel & {
  onOpen: (id: string) => void;
  onBack: () => void;
  onClose: () => void;
} {
  const [model] = useState(() => createEvidenceExplorerModel());
  const { publication, selectedId, onNavigate } = args;

  useEffect(() => {
    void model.load(() => fetchGraph(publication));
  }, [model, publication]);

  useEffect(() => {
    model.visit(selectedId);
  }, [model, selectedId]);

  const snapshot = useSyncExternalStore(model.subscribe, model.getSnapshot, model.getSnapshot);

  return {
    ...model.toViewModel(snapshot),
    onOpen: (id) => onNavigate(id),
    onBack: () => onNavigate(model.previous()),
    onClose: () => onNavigate(null),
  };
}
