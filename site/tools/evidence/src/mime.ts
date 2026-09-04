import { extname } from "node:path";

// Types MIME des fichiers de preuve, par extension. Les formats bureautiques
// et binaires sont proposés au téléchargement ; PDF, HTML, CSV et texte sont
// lisibles dans le site.
const MIME: Record<string, string> = {
  ".pdf": "application/pdf",
  ".html": "text/html; charset=utf-8",
  ".htm": "text/html; charset=utf-8",
  ".csv": "text/csv; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".md": "text/markdown; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
  ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ".xls": "application/vnd.ms-excel",
  ".zip": "application/zip",
  ".gz": "application/gzip",
  ".parquet": "application/vnd.apache.parquet",
  ".py": "text/x-python; charset=utf-8",
  ".yaml": "text/yaml; charset=utf-8",
  ".yml": "text/yaml; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
};

export function mimeOf(path: string): string {
  return MIME[extname(path).toLowerCase()] ?? "application/octet-stream";
}

export function languageOf(path: string): string {
  const ext = extname(path).toLowerCase();
  if (ext === ".py") return "python";
  if (ext === ".ts" || ext === ".tsx") return "typescript";
  if (ext === ".yaml" || ext === ".yml") return "yaml";
  if (ext === ".json") return "json";
  return "text";
}
