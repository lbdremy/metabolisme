import { resolve } from "node:path";

// Le site vit dans <dépôt>/site ; les études à côté (<dépôt>/logement…).
// Un chemin « de dépôt » est relatif à cette racine — c'est la forme
// enregistrée dans les manifestes, pour rester portable entre machines.
export const SITE_ROOT = resolve(import.meta.dirname, "../../..");
export const REPO_ROOT = process.env["METABOLISME_REPO"] ?? resolve(SITE_ROOT, "..");
export const CONTENT_DIR = resolve(SITE_ROOT, "content");

// Limite d'un asset statique Cloudflare (25 MiB) ; au-delà, stockage objet.
export const MAX_ASSET_BYTES = 25 * 1024 * 1024;

export function fail(message: string): never {
  console.error(message);
  process.exit(1);
}
