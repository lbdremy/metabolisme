import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { parse } from "yaml";
import { danglingReferences, PostSchema } from "@metabolisme/evidence";
import { CONTENT_DIR, fail, MAX_ASSET_BYTES, REPO_ROOT } from "./paths.ts";
import { PostConfigSchema, stripLeadingTitle } from "./post-config.ts";
import { asList, studyToGraph } from "./study-to-graph.ts";

// Construit le contenu publiable de chaque post depuis son étude :
//   content/posts/<slug>/post.yaml   (écrit à la main)
//   → post.json, article.md, graph.json, files.json (générés)
//
// Usage : pnpm content:posts

const postsDir = join(CONTENT_DIR, "posts");

function readYaml(path: string): unknown {
  if (!existsSync(path)) fail(`Fichier introuvable : ${path}`);
  return parse(readFileSync(path, "utf8"));
}

function buildPost(slug: string): void {
  const dir = join(postsDir, slug);
  const config = PostConfigSchema.parse(readYaml(join(dir, "post.yaml")));
  if (config.slug !== slug) fail(`${slug}/post.yaml : slug « ${config.slug} » ≠ dossier`);

  const studyDir = resolve(REPO_ROOT, config.study.dir);
  const registries = {
    sources: asList("sources.yaml", readYaml(join(studyDir, "sources/sources.yaml"))),
    definitions: asList("definitions.yaml", readYaml(join(studyDir, "sources/definitions.yaml"))),
    hypotheses: asList("hypotheses.yaml", readYaml(join(studyDir, "sources/hypotheses.yaml"))),
    claims: asList("claims.yaml", readYaml(join(studyDir, "evidence/claims.yaml"))),
  };

  const { graph, files } = studyToGraph(registries, {
    studyPrefix: `${config.study.dir.replace(/\/$/, "")}/`,
    version: config.version,
    statFile: (repoPath) => {
      const path = resolve(REPO_ROOT, repoPath);
      return existsSync(path) ? { size: statSync(path).size } : null;
    },
    maxAssetBytes: MAX_ASSET_BYTES,
  });

  // Les empreintes déclarées dans les registres sont RECALCULÉES ici : une
  // copie figée dont le sha256 ne correspond plus fait échouer le build
  // (méthode INTRO §7 ; la dérivation pure ne fait que recopier).
  for (const node of graph.nodes) {
    if (node.type !== "source") continue;
    for (const file of node.files) {
      if (file.checksum === undefined) continue;
      const manifest = files.find((f) => f.path === file.path);
      const repoPath = manifest?.from ?? `${config.study.dir}/${file.name}`;
      const absolute = resolve(REPO_ROOT, repoPath);
      if (!existsSync(absolute)) continue;
      const digest = `sha256:${createHash("sha256").update(readFileSync(absolute)).digest("hex")}`;
      if (digest !== file.checksum) {
        fail(`${slug} : empreinte de ${repoPath} (${node.id}) ≠ registre — ${digest}`);
      }
    }
  }

  const dangling = danglingReferences(graph);
  if (dangling.length > 0) {
    fail(
      `${slug} : références non résolues — ${dangling.map((d) => `${d.from}→${d.to}`).join(", ")}`,
    );
  }
  const missing = files.filter((file) => file.hosted === "none");
  for (const file of missing) {
    console.warn(`  ! ${file.from} introuvable — non publié`);
  }

  const articlePath = join(studyDir, config.article);
  if (!existsSync(articlePath)) fail(`Article introuvable : ${articlePath}`);
  const article = stripLeadingTitle(readFileSync(articlePath, "utf8"));

  const post = PostSchema.parse({
    slug: config.slug,
    title: config.title,
    subtitle: config.subtitle,
    date: config.date,
    summary: config.summary,
    study: { slug: config.study.slug, name: config.study.name, question: config.study.question },
    version: config.version,
  });

  writeFileSync(join(dir, "post.json"), `${JSON.stringify(post, null, 2)}\n`);
  writeFileSync(join(dir, "article.md"), article);
  writeFileSync(join(dir, "graph.json"), `${JSON.stringify(graph)}\n`);
  writeFileSync(join(dir, "files.json"), `${JSON.stringify(files, null, 2)}\n`);

  const large = files.filter((file) => file.hosted === "object-store").length;
  console.log(
    `✓ ${slug} — ${graph.nodes.length} nœuds, ${files.length} fichiers` +
      (large > 0 ? ` (${large} en stockage objet)` : ""),
  );
}

if (!existsSync(postsDir)) fail(`Dossier introuvable : ${postsDir}`);
const slugs = readdirSync(postsDir, { withFileTypes: true })
  .filter((entry) => entry.isDirectory() && existsSync(join(postsDir, entry.name, "post.yaml")))
  .map((entry) => entry.name)
  .toSorted();
if (slugs.length === 0) console.log("Aucun post (content/posts/<slug>/post.yaml).");
for (const slug of slugs) buildPost(slug);

// La page « méthode » du site est l'INTRO du dépôt, copiée telle quelle.
{
  const source = resolve(REPO_ROOT, "INTRO.md");
  if (existsSync(source)) {
    const pagesDir = join(CONTENT_DIR, "pages");
    mkdirSync(pagesDir, { recursive: true });
    writeFileSync(join(pagesDir, "methode.md"), readFileSync(source, "utf8"));
    console.log("✓ pages/methode.md ← INTRO.md");
  }
}
