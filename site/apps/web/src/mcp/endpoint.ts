import { createMcpHandler } from "@modelcontextprotocol/server";
import { EvidenceGraphSchema, selectReadable, tokensMatch } from "~/contracts/evidence";
import { indexedNotes, indexedPage, indexedPosts, mcpToken } from "~/content-index";
import { createMetabolismeMcpServer, type McpContent } from "./server";

// L'adresse du serveur MCP : /mcp/<jeton>. Comme une note, elle n'est
// protégée que par son jeton (HMAC du secret de build) ; un jeton faux est
// une page inexistante, pas un refus qui confirmerait que l'adresse existe.

export const MCP_PREFIX = "/mcp/";

// Les graphes sont des assets statiques : le Worker les lit par la même URL
// que le navigateur.
export type AssetFetcher = { fetch: (request: Request) => Promise<Response> };

function mcpContent(origin: string, assets: AssetFetcher): McpContent {
  return {
    origin,
    readables: selectReadable(indexedPosts(), indexedNotes()),
    method: indexedPage("methode")?.markdown,
    loadGraph: async (readable) => {
      const path = `/content/${readable.kind}s/${readable.contentId}/graph.json`;
      const response = await assets.fetch(new Request(new URL(path, origin)));
      if (!response.ok) {
        throw new Error(`Graphe de « ${readable.slug} » illisible (HTTP ${response.status}).`);
      }
      return EvidenceGraphSchema.parse(await response.json());
    },
  };
}

export function serveMcp(request: Request, assets: AssetFetcher): Promise<Response> | Response {
  const url = new URL(request.url);
  const token = url.pathname.slice(MCP_PREFIX.length).replace(/\/$/, "");
  if (!tokensMatch(mcpToken(), token)) {
    return new Response("Not found", { status: 404 });
  }
  const handler = createMcpHandler(
    () => createMetabolismeMcpServer(mcpContent(url.origin, assets)),
    {
      legacy: "stateless",
    },
  );
  return handler.fetch(request);
}
