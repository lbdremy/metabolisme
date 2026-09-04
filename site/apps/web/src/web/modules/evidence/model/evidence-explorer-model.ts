import { createModelStore, memoProjection } from "@metabolisme/web-core";
import {
  indexGraph,
  upstreamChain,
  type ChainStep,
  type EvidenceFile,
  type EvidenceGraph,
  type EvidenceNode,
  type GraphIndex,
} from "~/contracts/evidence";

// Modèle externe de l'explorateur de preuves : le graphe (chargé), le nœud
// ouvert, le fil des nœuds visités (pour « dépiler » puis revenir), et le
// fichier ouvert dans la visionneuse. Le nœud ouvert est aussi dans l'URL ;
// c'est la route qui le pousse ici (visit) — le modèle ne connaît pas le
// routeur.

// Le graphe indexé (des Map) vit hors du snapshot immuable : le snapshot ne
// porte que l'état de chargement, et change quand le graphe arrive.
export type GraphState =
  | { readonly status: "idle" }
  | { readonly status: "loading" }
  | { readonly status: "ready" }
  | { readonly status: "error"; readonly message: string };

export type OpenFile = {
  readonly nodeId: string;
  readonly file: EvidenceFile;
  readonly page: number | null;
};

export type EvidenceExplorerSnapshot = {
  readonly graph: GraphState;
  readonly selectedId: string | null;
  readonly trail: ReadonlyArray<string>;
  readonly openFile: OpenFile | null;
};

export type EvidenceExplorerViewModel = {
  readonly graphStatus: GraphState["status"];
  readonly errorMessage: string | null;
  readonly index: GraphIndex | null;
  readonly version: EvidenceGraph["version"] | null;
  readonly selected: EvidenceNode | null;
  readonly selectedMissing: boolean;
  readonly trail: ReadonlyArray<EvidenceNode>;
  readonly canGoBack: boolean;
  readonly chain: ReadonlyArray<ChainStep>;
  readonly openFile: OpenFile | null;
  readonly isKnown: (id: string) => boolean;
  readonly onOpenFile: (nodeId: string, file: EvidenceFile, page: number | null) => void;
  readonly onCloseFile: () => void;
};

export type EvidenceExplorerModel = {
  subscribe: (listener: () => void) => () => void;
  getSnapshot: () => EvidenceExplorerSnapshot;
  toViewModel: (snapshot: EvidenceExplorerSnapshot) => EvidenceExplorerViewModel;
  load: (loader: () => Promise<EvidenceGraph>) => Promise<void>;
  visit: (id: string | null) => void;
  previous: () => string | null;
  openFile: (nodeId: string, file: EvidenceFile, page: number | null) => void;
  closeFile: () => void;
};

export function createEvidenceExplorerModel(): EvidenceExplorerModel {
  const store = createModelStore<EvidenceExplorerSnapshot>({
    graph: { status: "idle" },
    selectedId: null,
    trail: [],
    openFile: null,
  });
  let loaded: { graph: EvidenceGraph; index: GraphIndex } | null = null;

  async function load(loader: () => Promise<EvidenceGraph>): Promise<void> {
    if (store.getSnapshot().graph.status !== "idle") return;
    store.update((draft) => {
      draft.graph = { status: "loading" };
    });
    try {
      const graph = await loader();
      loaded = { graph, index: indexGraph(graph) };
      store.update((draft) => {
        draft.graph = { status: "ready" };
      });
    } catch (cause) {
      store.update((draft) => {
        draft.graph = {
          status: "error",
          message: cause instanceof Error ? cause.message : "Chargement du graphe impossible.",
        };
      });
    }
  }

  // Le nœud ouvert vient de l'URL. Ouvrir un nœud l'ajoute au fil ; revenir
  // en arrière (previous) ne l'y remet pas ; fermer vide le fil.
  function visit(id: string | null): void {
    const current = store.getSnapshot();
    if (current.selectedId === id) return;
    store.update((draft) => {
      draft.selectedId = id;
      draft.openFile = null;
      if (id === null) {
        draft.trail = [];
        return;
      }
      const position = draft.trail.indexOf(id);
      // Revenir sur un nœud déjà dans le fil le tronque là (pas de boucle).
      draft.trail = position === -1 ? [...draft.trail, id] : draft.trail.slice(0, position + 1);
    });
  }

  function previous(): string | null {
    const { trail } = store.getSnapshot();
    return trail.length >= 2 ? (trail[trail.length - 2] ?? null) : null;
  }

  function openFile(nodeId: string, file: EvidenceFile, page: number | null): void {
    store.update((draft) => {
      draft.openFile = { nodeId, file, page };
    });
  }

  function closeFile(): void {
    if (store.getSnapshot().openFile === null) return;
    store.update((draft) => {
      draft.openFile = null;
    });
  }

  const toViewModel = memoProjection(
    (snapshot: EvidenceExplorerSnapshot): EvidenceExplorerViewModel => {
      const index = snapshot.graph.status === "ready" && loaded !== null ? loaded.index : null;
      const selected =
        index !== null && snapshot.selectedId !== null
          ? (index.byId.get(snapshot.selectedId) ?? null)
          : null;
      return {
        graphStatus: snapshot.graph.status,
        errorMessage: snapshot.graph.status === "error" ? snapshot.graph.message : null,
        index,
        version: snapshot.graph.status === "ready" && loaded !== null ? loaded.graph.version : null,
        selected,
        selectedMissing: index !== null && snapshot.selectedId !== null && selected === null,
        trail:
          index === null
            ? []
            : snapshot.trail.flatMap((id) => {
                const node = index.byId.get(id);
                return node === undefined ? [] : [node];
              }),
        canGoBack: snapshot.trail.length >= 2,
        chain: index !== null && selected !== null ? upstreamChain(index, selected.id) : [],
        openFile: snapshot.openFile,
        isKnown: (id) => index?.byId.has(id) ?? false,
        onOpenFile: openFile,
        onCloseFile: closeFile,
      };
    },
  );

  return {
    subscribe: store.subscribe,
    getSnapshot: store.getSnapshot,
    toViewModel,
    load,
    visit,
    previous,
    openFile,
    closeFile,
  };
}
