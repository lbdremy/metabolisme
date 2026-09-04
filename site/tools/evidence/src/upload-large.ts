import { spawnSync } from "node:child_process";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { FileManifestSchema } from "@metabolisme/evidence";
import { CONTENT_DIR, fail, NOTES_DIR, REPO_ROOT, SITE_ROOT } from "./paths.ts";

// Téléverse vers le stockage objet les fichiers de preuve trop lourds pour
// être des assets statiques (files.json : hosted = "object-store"). Le Worker
// les sert sous la même URL que les assets, /content/<kind>/<id>/files/<path>.
//
// Usage : pnpm --filter @metabolisme/tool-evidence upload-large [--dry-run]

const webDir = join(SITE_ROOT, "apps/web");
const wranglerConfig = join(webDir, "wrangler.jsonc");
const dryRun = process.argv.includes("--dry-run");

// Le nom du bucket est lu dans la configuration de l'application : une seule
// source de vérité.
function bucketName(): string {
  if (!existsSync(wranglerConfig)) fail(`Configuration introuvable : ${wranglerConfig}`);
  const match = /"bucket_name"\s*:\s*"([^"]+)"/.exec(readFileSync(wranglerConfig, "utf8"));
  if (match?.[1] === undefined) fail(`Aucun bucket_name dans ${wranglerConfig}.`);
  return match[1];
}

function humanSize(bytes: number): string {
  return `${(bytes / 1_000_000).toFixed(1)} Mo`;
}

function upload(bucket: string, key: string, filePath: string, mime: string, size: number): void {
  console.log(`→ ${key} (${humanSize(size)})`);
  if (dryRun) return;
  const result = spawnSync(
    "npx",
    [
      "wrangler",
      "r2",
      "object",
      "put",
      `${bucket}/${key}`,
      "--file",
      filePath,
      "--content-type",
      mime,
      // Sans --remote, wrangler écrit dans le stockage local de développement
      // en annonçant quand même « Upload complete ».
      "--remote",
    ],
    { stdio: "inherit", cwd: webDir },
  );
  if (result.error !== undefined) fail(`wrangler introuvable : ${result.error.message}`);
  if (result.status !== 0) fail(`Téléversement échoué : ${key}`);
}

const bucket = bucketName();
let count = 0;
for (const kind of ["posts", "notes"] as const) {
  const base = kind === "posts" ? join(CONTENT_DIR, "posts") : NOTES_DIR;
  if (!existsSync(base)) continue;
  for (const entry of readdirSync(base, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const manifestPath = join(base, entry.name, "files.json");
    if (!existsSync(manifestPath)) continue;
    const manifest = FileManifestSchema.parse(JSON.parse(readFileSync(manifestPath, "utf8")));
    for (const file of manifest) {
      if (file.hosted !== "object-store") continue;
      // Un fichier de post est relatif au dépôt ; un fichier de note, à son dossier.
      const source =
        kind === "posts" ? resolve(REPO_ROOT, file.from) : resolve(base, entry.name, file.from);
      if (!existsSync(source)) fail(`Fichier introuvable : ${source}`);
      upload(bucket, `${kind}/${entry.name}/files/${file.path}`, source, file.mime, file.size);
      count += 1;
    }
  }
}
console.log(
  count === 0
    ? "Rien à téléverser."
    : `${count} fichier(s) ${dryRun ? "à téléverser" : "téléversé(s)"}.`,
);
