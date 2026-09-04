import { createReadStream } from "node:fs";
import { readdir, readFile, stat } from "node:fs/promises";
import { extname, join, resolve } from "node:path";
import { deriveNoteToken } from "@metabolisme/evidence";
import { loadEnv, type Plugin } from "vite";

// Pont entre content/ (généré par tools/evidence) et l'application.
//
// Le runtime de déploiement (Cloudflare Workers) n'a pas de système de
// fichiers : rien ne peut être lu à la demande. Ce plugin résout le problème
// au build, en séparant deux natures de contenu :
//
//   - les métadonnées (post.json, note.json) sont minuscules et nécessaires
//     au rendu serveur des pages → module virtuel bundlé dans le Worker ;
//   - le reste (article, graphe, sources figées, code, sorties) est
//     volumineux et jamais nécessaire au serveur → assets statiques servis
//     par le CDN, sous /content/<posts|notes>/<id>/….
//
// Les fichiers de preuve ne sont pas copiés dans content/ : files.json dit
// où les prendre dans le dépôt (les sources figées vivent dans l'étude, en
// Git LFS). Au-delà de la taille d'un asset, un fichier est marqué
// « object-store » et téléversé à part (tools/evidence upload).
//
// En dev, un middleware sert les mêmes URL depuis le disque : une seule
// façon d'accéder au contenu, dev comme prod.

// Le secret qui dérive les jetons des notes (HMAC du slug). Sans lui, le
// build utilise une valeur de développement : les adresses ne sont alors pas
// secrètes — la production doit le fournir (NOTE_TOKEN_SECRET).
const DEV_NOTE_SECRET = "dev-only-note-secret";
let noteSecret = DEV_NOTE_SECRET;

const VIRTUAL_ID = "virtual:content-index";
const RESOLVED_VIRTUAL_ID = "\0" + VIRTUAL_ID;

export const CONTENT_ROUTE_PREFIX = "/content";

// Fichiers générés servis tels quels depuis le dossier de la publication.
const PUBLISHED_FILES: Record<"posts" | "notes", readonly string[]> = {
  posts: ["article.md", "graph.json"],
  notes: ["note.md", "graph.json"],
};

function siteRoot(): string {
  return resolve(process.cwd(), "../..");
}

function repoRoot(): string {
  const fromEnv = process.env["METABOLISME_REPO"];
  return fromEnv !== undefined ? resolve(fromEnv) : resolve(siteRoot(), "..");
}

function contentDir(): string {
  return join(siteRoot(), "content");
}

async function exists(path: string): Promise<boolean> {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

type Kind = "posts" | "notes";

type ManifestEntry = {
  readonly path: string;
  readonly from: string;
  readonly size: number;
  readonly mime: string;
  readonly hosted: "asset" | "object-store" | "none";
};

type Publication = {
  readonly kind: Kind;
  // Identifiant dans l'URL : slug d'un post, jeton d'une note.
  readonly id: string;
  // Dossier sur le disque (slug pour les deux).
  readonly slug: string;
  readonly dir: string;
  readonly meta: unknown;
  // Le texte lui-même entre dans l'index : il est rendu côté serveur (SEO,
  // lecture immédiate) et pèse quelques dizaines de Ko par publication.
  readonly markdown: string;
  readonly files: readonly ManifestEntry[];
};

async function readPublications(kind: Kind): Promise<Publication[]> {
  const base = join(contentDir(), kind);
  let entries;
  try {
    entries = await readdir(base, { withFileTypes: true });
  } catch {
    return [];
  }
  const metaFile = kind === "posts" ? "post.json" : "note.json";
  const publications = await Promise.all(
    entries
      .filter((entry) => entry.isDirectory())
      .map(async (entry): Promise<Publication | null> => {
        const dir = join(base, entry.name);
        let meta: unknown;
        try {
          meta = JSON.parse(await readFile(join(dir, metaFile), "utf8"));
        } catch {
          // Un dossier sans métadonnées générées n'est pas publié (post.yaml
          // seul, note en cours d'écriture) : on l'ignore sans casser le build.
          return null;
        }
        let files: ManifestEntry[] = [];
        try {
          files = JSON.parse(await readFile(join(dir, "files.json"), "utf8")) as ManifestEntry[];
        } catch {
          files = [];
        }
        let markdown = "";
        try {
          markdown = await readFile(join(dir, kind === "posts" ? "article.md" : "note.md"), "utf8");
        } catch {
          markdown = "";
        }
        const id = kind === "notes" ? await deriveNoteToken(noteSecret, entry.name) : entry.name;
        return { kind, id, slug: entry.name, dir, meta, markdown, files };
      }),
  );
  return publications
    .filter((publication): publication is Publication => publication !== null)
    .toSorted((a, b) => a.id.localeCompare(b.id));
}

// Pages statiques (la méthode…) : un Markdown par page dans content/pages/.
async function readPages(): Promise<{ slug: string; markdown: string }[]> {
  const base = join(contentDir(), "pages");
  let entries;
  try {
    entries = await readdir(base, { withFileTypes: true });
  } catch {
    return [];
  }
  return Promise.all(
    entries
      .filter((entry) => entry.isFile() && entry.name.endsWith(".md"))
      .map(async (entry) => ({
        slug: entry.name.slice(0, -3),
        markdown: await readFile(join(base, entry.name), "utf8"),
      })),
  );
}

const MIME: Record<string, string> = {
  ".json": "application/json; charset=utf-8",
  ".md": "text/markdown; charset=utf-8",
};

// Résout une URL /content/<kind>/<id>/<rest> vers un fichier du disque.
async function resolveContentFile(
  publications: Publication[],
  relative: string,
): Promise<{ path: string; mime: string } | null> {
  const [kind, id, ...rest] = relative.split("/");
  if ((kind !== "posts" && kind !== "notes") || id === undefined || rest.length === 0) return null;
  if (!/^[a-z0-9][a-z0-9-]*$/.test(id)) return null;
  // Les URL sont adressées par identifiant public (jeton pour une note).
  const publication = publications.find((p) => p.kind === kind && p.id === id);
  if (publication === undefined) return null;
  const file = rest.join("/");
  if (PUBLISHED_FILES[kind].includes(file)) {
    return { path: join(publication.dir, file), mime: MIME[extname(file)] ?? "text/plain" };
  }
  if (rest[0] === "files") {
    const logical = rest.slice(1).join("/");
    const entry = publication.files.find((f) => f.path === logical && f.hosted !== "none");
    if (entry === undefined) return null;
    return { path: resolve(repoRoot(), entry.from), mime: entry.mime };
  }
  return null;
}

function parseRange(
  header: string | undefined,
  size: number,
): { start: number; end: number } | null {
  const match = header === undefined ? null : /^bytes=(\d*)-(\d*)$/.exec(header);
  if (match === null) return null;
  const [, rawStart, rawEnd] = match;
  if (rawStart === "" && rawEnd === "") return null;
  const start = rawStart === "" ? size - Number(rawEnd) : Number(rawStart);
  const end = rawStart !== "" && rawEnd !== "" ? Number(rawEnd) : size - 1;
  if (Number.isNaN(start) || Number.isNaN(end) || start > end || start < 0) return null;
  return { start: Math.max(0, start), end: Math.min(end, size - 1) };
}

export function contentAssets(): Plugin {
  return {
    name: "metabolisme:content-assets",

    config(_config, { mode }) {
      const env = loadEnv(mode, siteRoot(), "");
      const secret = env["NOTE_TOKEN_SECRET"] ?? process.env["NOTE_TOKEN_SECRET"];
      if (secret !== undefined && secret !== "") {
        noteSecret = secret;
      } else if (mode === "production") {
        console.warn(
          "[content] NOTE_TOKEN_SECRET absent : les adresses des notes ne seront PAS secrètes.",
        );
      }
    },

    resolveId(id) {
      return id === VIRTUAL_ID ? RESOLVED_VIRTUAL_ID : null;
    },

    async load(id) {
      if (id !== RESOLVED_VIRTUAL_ID) return null;
      const [posts, notes, pages] = await Promise.all([
        readPublications("posts"),
        readPublications("notes"),
        readPages(),
      ]);
      const index = {
        posts: posts.map((p) => ({ slug: p.id, post: p.meta, markdown: p.markdown })),
        notes: notes.map((n) => ({ token: n.id, note: n.meta, markdown: n.markdown })),
        pages,
      };
      return `export const contentIndex = ${JSON.stringify(index)};\n`;
    },

    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = req.url ?? "";
        if (!url.startsWith(CONTENT_ROUTE_PREFIX + "/")) return next();
        let relative: string;
        try {
          relative = decodeURIComponent(
            url.slice(CONTENT_ROUTE_PREFIX.length + 1).split("?")[0] ?? "",
          );
        } catch {
          res.statusCode = 404;
          return res.end("Not found");
        }
        void (async () => {
          const publications = [
            ...(await readPublications("posts")),
            ...(await readPublications("notes")),
          ];
          const resolved = await resolveContentFile(publications, relative);
          if (resolved === null || !(await exists(resolved.path))) {
            server.config.logger.warn(
              `[content] 404 ${relative} — ${resolved === null ? `non résolu (${publications.length} publications, cwd ${process.cwd()})` : resolved.path}`,
            );
            res.statusCode = 404;
            return res.end("Not found");
          }
          const size = (await stat(resolved.path)).size;
          const range = parseRange(req.headers["range"], size);
          if (range === null) {
            res.writeHead(200, {
              "Content-Type": resolved.mime,
              "Content-Length": String(size),
              "Accept-Ranges": "bytes",
            });
            return createReadStream(resolved.path).pipe(res);
          }
          res.writeHead(206, {
            "Content-Type": resolved.mime,
            "Content-Length": String(range.end - range.start + 1),
            "Content-Range": `bytes ${range.start}-${range.end}/${size}`,
            "Accept-Ranges": "bytes",
          });
          createReadStream(resolved.path, { start: range.start, end: range.end }).pipe(res);
        })();
      });
    },

    // Seul le build client produit les fichiers servis par le CDN ; les
    // émettre aussi côté serveur les ferait entrer dans le bundle du Worker.
    async generateBundle() {
      if (this.environment.name !== "client") return;
      const publications = [
        ...(await readPublications("posts")),
        ...(await readPublications("notes")),
      ];
      for (const publication of publications) {
        for (const file of PUBLISHED_FILES[publication.kind]) {
          const path = join(publication.dir, file);
          if (!(await exists(path))) continue;
          this.emitFile({
            type: "asset",
            fileName: `content/${publication.kind}/${publication.id}/${file}`,
            source: await readFile(path),
          });
        }
        for (const entry of publication.files) {
          if (entry.hosted !== "asset") continue;
          const path = resolve(repoRoot(), entry.from);
          if (!(await exists(path))) {
            this.warn(`${entry.from} introuvable — non publié`);
            continue;
          }
          this.emitFile({
            type: "asset",
            fileName: `content/${publication.kind}/${publication.id}/files/${entry.path}`,
            source: await readFile(path),
          });
        }
      }
    },
  };
}
