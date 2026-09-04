// Formats d'affichage du panneau (français) : tailles, nombres, dates.

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} o`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} Ko`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} Mo`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} Go`;
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat("fr-FR", { maximumFractionDigits: 4 }).format(value);
}

const MONTHS = [
  "janvier",
  "février",
  "mars",
  "avril",
  "mai",
  "juin",
  "juillet",
  "août",
  "septembre",
  "octobre",
  "novembre",
  "décembre",
];

// « 2026-08-10 » → « 10 août 2026 » ; toute autre forme est rendue telle quelle.
export function formatDate(value: string): string {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (match === null) return value;
  const [, year, month, day] = match;
  const monthName = MONTHS[Number(month) - 1];
  if (monthName === undefined || day === undefined) return value;
  return `${Number(day)} ${monthName} ${year}`;
}

export const CONFIDENCE_LABEL: Record<"low" | "medium" | "high", string> = {
  low: "faible",
  medium: "moyenne",
  high: "élevée",
};

// Qui peut être lu dans le site, et comment.
export type ViewerKind = "pdf" | "html" | "csv" | "json" | "text" | "code" | "download";

export function viewerKindOf(mime: string, path: string): ViewerKind {
  if (mime.startsWith("application/pdf")) return "pdf";
  if (mime.startsWith("text/html")) return "html";
  if (mime.startsWith("text/csv")) return "csv";
  if (mime.startsWith("application/json")) return "json";
  if (mime.startsWith("text/x-python") || /\.(py|ts|yaml|yml)$/.test(path)) return "code";
  if (mime.startsWith("text/") || mime.startsWith("application/xml")) return "text";
  return "download";
}
