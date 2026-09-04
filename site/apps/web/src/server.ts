import handler, { createServerEntry } from "@tanstack/react-start/server-entry";
import { env } from "cloudflare:workers";

// Point d'entrée serveur.
//
// Le site est public : pas d'authentification. Les notes partageables ne
// sont protégées que par leur URL non devinable — et signalées « noindex »
// pour ne pas être référencées.
//
// Les fichiers de preuve (/content/…) sont des assets statiques servis par
// le CDN, sauf les plus lourds (> 25 Mio) qui vivent dans un stockage objet :
// quand l'asset n'existe pas, on tente le bucket avec le même chemin.

const CONTENT_PREFIX = "/content/";

// Une seule adresse canonique : www renvoie sur l'apex.
const CANONICAL_HOST = "metabolisme.dev";

async function serveLargeFile(request: Request, key: string): Promise<Response> {
  const object = await env.EVIDENCE_FILES.get(key, {
    range: request.headers,
    onlyIf: request.headers,
  });
  if (object === null) {
    return new Response("Not found", { status: 404 });
  }
  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set("ETag", object.httpEtag);
  headers.set("Accept-Ranges", "bytes");
  // Une source figée ne change plus (son empreinte est publiée) : cache long.
  headers.set("Cache-Control", "public, max-age=31536000, immutable");
  if (!("body" in object)) {
    const revalidating =
      request.headers.has("if-none-match") || request.headers.has("if-modified-since");
    return new Response(null, { status: revalidating ? 304 : 412, headers });
  }
  if (object.range !== undefined && "offset" in object.range && request.headers.has("range")) {
    const offset = object.range.offset ?? 0;
    const length = object.range.length ?? object.size - offset;
    headers.set("Content-Range", `bytes ${offset}-${offset + length - 1}/${object.size}`);
    headers.set("Content-Length", String(length));
    return new Response(object.body, { status: 206, headers });
  }
  headers.set("Content-Length", String(object.size));
  return new Response(object.body, { status: 200, headers });
}

export default createServerEntry({
  async fetch(request) {
    const url = new URL(request.url);
    if (url.hostname === `www.${CANONICAL_HOST}`) {
      url.hostname = CANONICAL_HOST;
      return Response.redirect(url.toString(), 301);
    }
    const { pathname } = url;
    if (pathname.startsWith(CONTENT_PREFIX)) {
      const fromAssets = await env.ASSETS.fetch(request);
      if (fromAssets.status !== 404) return fromAssets;
      return serveLargeFile(request, decodeURIComponent(pathname.slice(CONTENT_PREFIX.length)));
    }
    return handler.fetch(request);
  },
});
