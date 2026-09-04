import { EvidenceGraphSchema, type EvidenceGraph } from "~/contracts/evidence";

// Le contenu volumineux d'une publication (article, graphe, fichiers de
// preuve) est immuable une fois généré : servi comme fichier statique (CDN en
// production, middleware Vite en dev), jamais rendu par le serveur. Ces
// fonctions s'exécutent côté navigateur.

const CONTENT_BASE = "/content";

export type PublicationRef = {
  readonly kind: "posts" | "notes";
  readonly id: string;
};

function baseUrl(ref: PublicationRef): string {
  return `${CONTENT_BASE}/${ref.kind}/${ref.id}`;
}

export function contentFileUrl(ref: PublicationRef, logicalPath: string): string {
  return `${baseUrl(ref)}/files/${logicalPath.split("/").map(encodeURIComponent).join("/")}`;
}

async function fetchText(url: string): Promise<string> {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Lecture de ${url} impossible (HTTP ${response.status})`);
  }
  return response.text();
}

export function fetchMarkdown(ref: PublicationRef): Promise<string> {
  return fetchText(`${baseUrl(ref)}/${ref.kind === "posts" ? "article.md" : "note.md"}`);
}

export async function fetchGraph(ref: PublicationRef): Promise<EvidenceGraph> {
  const raw: unknown = JSON.parse(await fetchText(`${baseUrl(ref)}/graph.json`));
  return EvidenceGraphSchema.parse(raw);
}
