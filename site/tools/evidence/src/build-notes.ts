import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { parse } from "yaml";
import { deriveNoteToken, NoteSchema } from "@metabolisme/evidence";
import { noteToGraph } from "./note-to-graph.ts";
import { CONTENT_DIR, fail } from "./paths.ts";

// Compile les notes partageables :
//   content/notes/<slug>/note.yaml, note.md, evidence.yaml, sources/…  (main)
//   → note.json, graph.json, files.json                                 (générés)
//
// Usage : pnpm content:notes                 compile toutes les notes
//         pnpm --filter @metabolisme/tool-evidence new-note <slug>
//         pnpm --filter @metabolisme/tool-evidence note-url <slug>
//
// L'adresse publique d'une note porte un jeton dérivé du slug et du secret
// NOTE_TOKEN_SECRET (variable d'environnement, ou site/.env) : le dépôt ne
// la révèle pas. `note-url` l'affiche, avec NOTE_SITE_URL comme base.

const notesDir = join(CONTENT_DIR, "notes");
const SLUG = /^[a-z0-9][a-z0-9-]*$/;

function sha256(path: string): string {
  return `sha256:${createHash("sha256").update(readFileSync(path)).digest("hex")}`;
}

function readYaml(path: string): unknown {
  if (!existsSync(path)) fail(`Fichier introuvable : ${path}`);
  return parse(readFileSync(path, "utf8"));
}

function buildNote(slug: string): boolean {
  const dir = join(notesDir, slug);
  const note = NoteSchema.parse({ slug, ...(readYaml(join(dir, "note.yaml")) as object) });
  const markdownPath = join(dir, "note.md");
  if (!existsSync(markdownPath)) fail(`${slug} : note.md manquant`);
  const markdown = readFileSync(markdownPath, "utf8");

  const { graph, files, problems } = noteToGraph(readYaml(join(dir, "evidence.yaml")), markdown, {
    version: note.version,
    notePrefix: `site/content/notes/${slug}/`,
    readFile: (relativePath) => {
      const path = join(dir, relativePath);
      return existsSync(path) ? { size: statSync(path).size, checksum: sha256(path) } : null;
    },
  });

  for (const problem of problems) console.error(`  ✗ ${slug} — ${problem.message}`);
  if (problems.length > 0) return false;

  writeFileSync(join(dir, "note.json"), `${JSON.stringify(note, null, 2)}\n`);
  writeFileSync(join(dir, "graph.json"), `${JSON.stringify(graph)}\n`);
  writeFileSync(join(dir, "files.json"), `${JSON.stringify(files, null, 2)}\n`);
  console.log(`✓ note ${slug} — ${graph.nodes.length} nœuds, ${files.length} fichiers`);
  return true;
}

const [command, argument] = process.argv.slice(2);

if (command === "--new") {
  if (argument === undefined || !SLUG.test(argument)) fail("Usage : new-note <slug>");
  const dir = join(notesDir, argument);
  if (existsSync(dir)) fail(`La note ${argument} existe déjà.`);
  mkdirSync(join(dir, "sources"), { recursive: true });
  writeFileSync(
    join(dir, "note.yaml"),
    `title: Titre de la note\ndate: ${new Date().toISOString().slice(0, 10)}\ncontext: >\n  À qui, à quelle occasion.\n`,
  );
  writeFileSync(join(dir, "note.md"), "Texte de la note, avec des [ancres](ev:O-01).\n");
  writeFileSync(join(dir, "evidence.yaml"), "nodes: []\n");
  console.log(`Note créée : content/notes/${argument}/`);
  process.exit(0);
}

if (command === "--url") {
  if (argument === undefined || !SLUG.test(argument)) fail("Usage : note-url <slug>");
  const secret = process.env["NOTE_TOKEN_SECRET"];
  if (secret === undefined || secret === "") {
    fail("NOTE_TOKEN_SECRET absent : définissez-le (site/.env ou environnement).");
  }
  const base = (process.env["NOTE_SITE_URL"] ?? "https://metabolisme.example").replace(/\/$/, "");
  console.log(`${base}/notes/${await deriveNoteToken(secret, argument)}`);
  process.exit(0);
}

if (!existsSync(notesDir)) mkdirSync(notesDir, { recursive: true });
const slugs = readdirSync(notesDir, { withFileTypes: true })
  .filter((entry) => entry.isDirectory() && existsSync(join(notesDir, entry.name, "note.yaml")))
  .map((entry) => entry.name)
  .toSorted();
if (slugs.length === 0) console.log("Aucune note (content/notes/<slug>/note.yaml).");
let ok = true;
for (const slug of slugs) ok = buildNote(slug) && ok;
if (!ok) process.exit(1);
