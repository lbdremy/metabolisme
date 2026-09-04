import { ArrowLeft, Download, ExternalLink } from "lucide-react";
import { useEffect, useState } from "react";
import type { EvidenceFile } from "~/contracts/evidence";
import { contentFileUrl, type PublicationRef } from "~/content-assets/public";
import { IconButton } from "~/web/components/ui/icon-button";
import { highlightToHtml } from "~/web/lib/highlight";
import { previewCsv, type CsvPreview } from "../model/csv-preview";
import { formatBytes, viewerKindOf } from "../model/format";

// Lecture d'un fichier de preuve DANS le site : PDF (visionneuse du
// navigateur, à la page demandée), page HTML figée (isolée), CSV (aperçu des
// premières lignes), JSON (arbre), code (coloré), texte. Le reste se
// télécharge. L'URL d'origine reste toujours à un clic.

type Loaded<T> =
  | { status: "loading" }
  | { status: "ready"; value: T }
  | { status: "error"; message: string };

function useFetched<T>(
  url: string,
  read: (response: Response) => Promise<T>,
  headers?: HeadersInit,
) {
  const [state, setState] = useState<Loaded<T>>({ status: "loading" });
  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading" });
    fetch(url, headers === undefined ? undefined : { headers })
      .then(async (response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return read(response);
      })
      .then((value) => {
        if (!cancelled) setState({ status: "ready", value });
      })
      .catch((cause: unknown) => {
        if (!cancelled) {
          setState({
            status: "error",
            message: cause instanceof Error ? cause.message : "Lecture impossible",
          });
        }
      });
    return () => {
      cancelled = true;
    };
    // `read` et `headers` sont stables par type de visionneuse.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url]);
  return state;
}

function Status({ state }: { state: Loaded<unknown> }) {
  if (state.status === "loading")
    return <p className="p-4 font-sans text-sm text-ink-3">Chargement…</p>;
  if (state.status === "error")
    return <p className="p-4 font-sans text-sm text-status-interpretation">{state.message}</p>;
  return null;
}

const CSV_SAMPLE_BYTES = 256 * 1024;

// Les fichiers publics français sont souvent en Latin-1 : on tente UTF-8
// strictement, et on retombe sur windows-1252 si les octets ne passent pas.
function decodeText(bytes: ArrayBuffer): string {
  try {
    return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  } catch {
    return new TextDecoder("windows-1252").decode(bytes);
  }
}

function CsvView({ url, size }: { url: string; size: number }) {
  const complete = size <= CSV_SAMPLE_BYTES;
  const state = useFetched<CsvPreview>(
    url,
    async (response) =>
      previewCsv(decodeText(await response.arrayBuffer()), { maxRows: 60, complete }),
    complete ? undefined : { Range: `bytes=0-${CSV_SAMPLE_BYTES - 1}` },
  );
  if (state.status !== "ready") return <Status state={state} />;
  const { header, rows, truncated } = state.value;
  return (
    <div className="min-h-0 grow overflow-auto">
      <table className="min-w-full border-collapse font-mono text-[0.7rem]">
        <thead className="sticky top-0 bg-paper-2">
          <tr>
            {header.map((cell, i) => (
              <th
                key={i}
                className="whitespace-nowrap border-b border-rule px-2 py-1 text-left font-semibold"
              >
                {cell}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, r) => (
            <tr key={r} className="odd:bg-white/50">
              {row.map((cell, c) => (
                <td
                  key={c}
                  className="whitespace-nowrap border-b border-rule/60 px-2 py-0.5 tabular-nums"
                >
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {truncated && (
        <p className="p-3 font-sans text-[0.75rem] text-ink-3">
          Aperçu des premières lignes seulement — le fichier complet se télécharge ci-dessus.
        </p>
      )}
    </div>
  );
}

function JsonNode({ name, value, depth }: { name: string | null; value: unknown; depth: number }) {
  const label = name === null ? null : <span className="text-status-source">{name}</span>;
  if (value !== null && typeof value === "object") {
    const entries = Array.isArray(value)
      ? value.map((item, i) => [String(i), item] as const)
      : Object.entries(value);
    return (
      <details open={depth < 2} className="pl-3">
        <summary className="cursor-pointer select-none text-ink-2">
          {label}
          {label !== null && ": "}
          <span className="text-ink-3">
            {Array.isArray(value) ? `[${entries.length}]` : `{${entries.length}}`}
          </span>
        </summary>
        {entries.map(([key, item]) => (
          <JsonNode key={key} name={key} value={item} depth={depth + 1} />
        ))}
      </details>
    );
  }
  return (
    <div className="pl-3">
      {label}
      {label !== null && ": "}
      <span className={typeof value === "number" ? "tabular-nums text-status-result" : "text-ink"}>
        {typeof value === "string" ? `"${value}"` : String(value)}
      </span>
    </div>
  );
}

function JsonView({ url }: { url: string }) {
  const state = useFetched<unknown>(url, (response) => response.json());
  if (state.status !== "ready") return <Status state={state} />;
  return (
    <div className="min-h-0 grow overflow-auto p-3 font-mono text-[0.74rem] leading-relaxed">
      <JsonNode name={null} value={state.value} depth={0} />
    </div>
  );
}

function CodeView({ url, language }: { url: string; language: string }) {
  const state = useFetched<string>(url, async (response) =>
    highlightToHtml(await response.text(), language),
  );
  if (state.status !== "ready") return <Status state={state} />;
  // HTML produit par shiki à partir d'un fichier du dépôt : contenu maîtrisé.
  return (
    <div
      className="min-h-0 grow overflow-auto px-3 py-2 [&_pre]:whitespace-pre"
      dangerouslySetInnerHTML={{ __html: state.value }}
    />
  );
}

function TextView({ url }: { url: string }) {
  const state = useFetched<string>(url, async (response) =>
    decodeText(await response.arrayBuffer()),
  );
  if (state.status !== "ready") return <Status state={state} />;
  return (
    <pre className="min-h-0 grow overflow-auto whitespace-pre-wrap p-3 font-mono text-[0.74rem] leading-relaxed">
      {state.value}
    </pre>
  );
}

export function FileViewer({
  publication,
  file,
  page,
  originalUrl,
  language,
  onBack,
}: {
  publication: PublicationRef;
  file: EvidenceFile;
  page: number | null;
  originalUrl: string | null;
  language: string | null;
  onBack: () => void;
}) {
  const url = contentFileUrl(publication, file.path);
  const kind = viewerKindOf(file.mime, file.path);
  return (
    <div className="flex min-h-0 grow flex-col">
      <div className="flex items-center gap-1 border-b border-rule px-2 py-1.5">
        <IconButton icon={ArrowLeft} label="Revenir au nœud" onClick={onBack} />
        <span className="min-w-0 grow truncate font-mono text-[0.75rem]" title={file.path}>
          {file.name}
        </span>
        <span className="shrink-0 font-sans text-[0.7rem] text-ink-3">
          {formatBytes(file.size)}
        </span>
        {file.hosted !== "none" && (
          <a
            href={url}
            download={file.name}
            aria-label="Télécharger la copie figée"
            className="rounded-md p-1.5 text-ink-3 hover:bg-paper-2 hover:text-ink"
          >
            <Download aria-hidden className="size-4" />
          </a>
        )}
        {originalUrl !== null && (
          <a
            href={originalUrl}
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Ouvrir le document d'origine"
            className="rounded-md p-1.5 text-ink-3 hover:bg-paper-2 hover:text-ink"
          >
            <ExternalLink aria-hidden className="size-4" />
          </a>
        )}
      </div>
      {file.hosted === "none" ? (
        <p className="p-4 font-sans text-sm text-ink-2">
          Ce fichier n'est pas redistribué par le site ; il reste consultable à son adresse
          d'origine.
        </p>
      ) : kind === "pdf" ? (
        <>
          <iframe
            title={file.name}
            src={page === null ? url : `${url}#page=${page}`}
            className="min-h-0 grow bg-white"
          />
          <p className="shrink-0 border-t border-rule px-3 py-1.5 font-sans text-[0.7rem] text-ink-3">
            {page !== null && `Page ${page}. `}
            Si le document ne s'affiche pas,{" "}
            <a
              href={page === null ? url : `${url}#page=${page}`}
              target="_blank"
              rel="noopener noreferrer"
              className="underline"
            >
              l'ouvrir dans un onglet
            </a>
            .
          </p>
        </>
      ) : kind === "html" ? (
        <iframe title={file.name} src={url} sandbox="" className="min-h-0 grow bg-white" />
      ) : kind === "csv" ? (
        <CsvView url={url} size={file.size} />
      ) : kind === "json" ? (
        <JsonView url={url} />
      ) : kind === "code" ? (
        <CodeView url={url} language={language ?? "text"} />
      ) : kind === "text" ? (
        <TextView url={url} />
      ) : (
        <div className="p-4 font-sans text-sm text-ink-2">
          <p>Ce format ({file.mime.split(";")[0]}) ne se lit pas dans le navigateur.</p>
          <a
            href={url}
            download={file.name}
            className="mt-3 inline-flex items-center gap-2 underline"
          >
            <Download aria-hidden className="size-4" /> Télécharger la copie figée (
            {formatBytes(file.size)})
          </a>
        </div>
      )}
    </div>
  );
}
