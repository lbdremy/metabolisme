import { createMcpHandler } from "@modelcontextprotocol/server";
import { describe, expect, it } from "vitest";
import { EvidenceGraphSchema, type Readable } from "~/contracts/evidence";
import { createMetabolismeMcpServer } from "./server";

const graph = EvidenceGraphSchema.parse({
  nodes: [
    { id: "S-01", type: "source", title: "INSEE", publisher: "INSEE", source_url: "https://x" },
    { id: "O-01", type: "observation", title: "o", depends_on: ["S-01"] },
    { id: "L-01", type: "limit", title: "l" },
    { id: "R-01", type: "result", title: "r", depends_on: ["O-01"], limitations: ["L-01"] },
  ],
});

const readables: Readable[] = [
  {
    kind: "post",
    slug: "etude",
    title: "Étude",
    date: "2026-09-01",
    path: "/posts/etude",
    contentId: "etude",
    markdown: "La préemption (R-01).",
    status: "in_review",
  },
  {
    kind: "note",
    slug: "livret-un",
    title: "Livret, un",
    date: "2026-09-20",
    path: "/notes/tok",
    contentId: "tok",
    markdown: "Doctrine.",
    collection: { slug: "livret", title: "Livret 2027", position: 1 },
  },
];

const handler = createMcpHandler(
  () =>
    createMetabolismeMcpServer({
      origin: "https://metabolisme.dev",
      readables,
      method: "# Méthode",
      loadGraph: async () => graph,
    }),
  { legacy: "stateless" },
);

type RpcResult = {
  tools?: { name: string; annotations?: { readOnlyHint?: boolean } }[];
  isError?: boolean;
  content?: { type: string; text: string }[];
};

async function rpc(method: string, params: unknown): Promise<RpcResult> {
  const response = await handler.fetch(
    new Request("https://metabolisme.dev/mcp/x", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json, text/event-stream",
        "MCP-Protocol-Version": "2025-06-18",
      },
      body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
    }),
  );
  const body = await response.text();
  // Réponse JSON directe, ou un flux SSE d'un seul message.
  const payload = body.startsWith("{") ? body : (/^data: (.*)$/m.exec(body)?.[1] ?? "");
  return (JSON.parse(payload) as { result: RpcResult }).result;
}

async function call(name: string, args: Record<string, unknown>) {
  const result = await rpc("tools/call", { name, arguments: args });
  return { isError: result.isError === true, text: result.content?.map((c) => c.text) ?? [] };
}

describe("serveur MCP", () => {
  it("n'expose que des outils en lecture seule", async () => {
    const { tools = [] } = await rpc("tools/list", {});
    expect(tools.map((tool) => tool.name).toSorted()).toEqual([
      "get_graph",
      "list_publications",
      "read_method",
      "read_publication",
      "search",
      "walk_graph",
    ]);
    expect(tools.every((tool) => tool.annotations?.readOnlyHint === true)).toBe(true);
  });

  it("liste les publications avec leur adresse, filtrées par type", async () => {
    const { text } = await call("list_publications", { kind: "note" });
    expect(JSON.parse(text[0] ?? "[]")).toEqual([
      expect.objectContaining({ slug: "livret-un", url: "https://metabolisme.dev/notes/tok" }),
    ]);
  });

  it("lit une publication : métadonnées puis Markdown", async () => {
    const { text } = await call("read_publication", { slug: "etude" });
    expect(JSON.parse(text[0] ?? "{}")).toMatchObject({ status: "in_review" });
    expect(text[1]).toBe("La préemption (R-01).");
  });

  it("répond par une erreur, pas une exception, à un slug inconnu", async () => {
    const result = await call("read_publication", { slug: "note-privee" });
    expect(result.isError).toBe(true);
  });

  it("renvoie le graphe en JSON, filtrable par statut", async () => {
    const { text } = await call("get_graph", { slug: "etude", types: ["source", "limit"] });
    const payload = JSON.parse(text[0] ?? "{}") as { node_count: number; nodes: { id: string }[] };
    expect(payload.node_count).toBe(4);
    expect(payload.nodes.map((node) => node.id)).toEqual(["S-01", "L-01"]);
  });

  it("remonte la chaîne jusqu'aux sources, avec les limites rencontrées", async () => {
    const { text } = await call("walk_graph", { slug: "etude", node_id: "R-01" });
    const payload = JSON.parse(text[0] ?? "{}") as {
      steps: { depth: number; node: { id: string } }[];
      limits: { id: string }[];
    };
    expect(payload.steps.map((step) => [step.depth, step.node.id])).toEqual([
      [1, "O-01"],
      [2, "S-01"],
    ]);
    expect(payload.limits.map((limit) => limit.id)).toEqual(["L-01"]);
  });

  it("descend vers ce qu'un nœud soutient", async () => {
    const { text } = await call("walk_graph", {
      slug: "etude",
      node_id: "S-01",
      direction: "downstream",
    });
    const payload = JSON.parse(text[0] ?? "{}") as { steps: { node: { id: string } }[] };
    expect(payload.steps.map((step) => step.node.id)).toEqual(["O-01", "R-01"]);
  });

  it("cherche sans tenir compte des accents", async () => {
    const { text } = await call("search", { query: "preemption" });
    expect(JSON.parse(text[0] ?? "[]")).toEqual([
      expect.objectContaining({ slug: "etude", url: "https://metabolisme.dev/posts/etude" }),
    ]);
  });
});
