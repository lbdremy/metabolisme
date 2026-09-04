import { resolve } from "node:path";

// Le site vit dans <dépôt>/site ; les études à côté (<dépôt>/logement…).
// Un chemin « de dépôt » est relatif à cette racine — c'est la forme
// enregistrée dans les manifestes, pour rester portable entre machines.
export const SITE_ROOT = resolve(import.meta.dirname, "../../..");
export const REPO_ROOT = process.env["METABOLISME_REPO"] ?? resolve(SITE_ROOT, "..");
export const CONTENT_DIR = resolve(SITE_ROOT, "content");

// Les notes vivent dans un dépôt PRIVÉ séparé (metabolisme-notes), cloné à
// côté du dépôt public par défaut : leur contenu ne transite jamais par le
// dépôt du site.
export const NOTES_DIR =
  process.env["METABOLISME_NOTES_DIR"] ?? resolve(REPO_ROOT, "../metabolisme-notes");

// Limite d'un asset statique Cloudflare (25 MiB) ; au-delà, stockage objet.
export const MAX_ASSET_BYTES = 25 * 1024 * 1024;

export function fail(message: string): never {
  console.error(message);
  process.exit(1);
}
