import { ExternalLink, FileText, Quote } from "lucide-react";
import type { ReactNode } from "react";
import type {
  ComputedNode,
  DefinitionNode,
  EvidenceFile,
  HypothesisNode,
  Locator,
  ObservationNode,
  SourceNode,
} from "~/contracts/evidence";
import { isQuantifiedHypothesis } from "~/contracts/evidence";
import { cn } from "~/web/lib/cn";
import { CONFIDENCE_LABEL, formatBytes, formatDate, formatNumber } from "../model/format";

// Le corps du panneau selon le statut du nœud : ce qu'il faut montrer pour
// qu'un lecteur puisse vérifier — les métadonnées et fichiers d'une source,
// le texte d'une définition, la valeur et la plage d'une hypothèse, la
// citation et la page d'une observation, le code et la sortie d'un calcul.

export type OpenFileCommand = (file: EvidenceFile, page: number | null) => void;

export function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="grid grid-cols-[7.5rem_1fr] gap-x-3 gap-y-0.5 font-sans text-[0.8rem]">
      <dt className="text-ink-3">{label}</dt>
      <dd className="min-w-0 break-words text-ink">{children}</dd>
    </div>
  );
}

export function Section({
  title,
  children,
  className,
}: {
  title: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={cn("mt-5", className)}>
      <h3 className="mb-2 font-sans text-[0.68rem] font-semibold uppercase tracking-wider text-ink-3">
        {title}
      </h3>
      {children}
    </section>
  );
}

export function ExternalAnchor({ href, children }: { href: string; children: ReactNode }) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-1 text-status-definition underline decoration-1 underline-offset-2 hover:text-ink"
    >
      {children}
      <ExternalLink aria-hidden className="size-3 shrink-0" />
    </a>
  );
}

function FileRow({
  file,
  onOpen,
  page,
}: {
  file: EvidenceFile;
  onOpen: OpenFileCommand;
  page: number | null;
}) {
  const readable = file.hosted !== "none";
  return (
    <li>
      <button
        type="button"
        disabled={!readable}
        onClick={() => onOpen(file, page)}
        className={cn(
          "flex w-full items-center gap-2 rounded-md border border-rule bg-white/60 px-2.5 py-1.5 text-left",
          "font-sans text-[0.8rem] transition-colors hover:border-rule-2 hover:bg-white",
          "disabled:cursor-not-allowed disabled:opacity-60",
        )}
      >
        <FileText aria-hidden className="size-4 shrink-0 text-ink-3" />
        <span className="min-w-0 grow truncate font-mono text-[0.75rem]">{file.name}</span>
        <span className="shrink-0 text-[0.7rem] text-ink-3">
          {readable ? formatBytes(file.size) : "non redistribué"}
        </span>
      </button>
      {file.checksum !== undefined && (
        <p
          className="mt-0.5 truncate pl-2 font-mono text-[0.62rem] text-ink-3"
          title={file.checksum}
        >
          {file.checksum}
        </p>
      )}
    </li>
  );
}

export function SourceBody({
  node,
  onOpenFile,
}: {
  node: SourceNode;
  onOpenFile: OpenFileCommand;
}) {
  return (
    <>
      <dl className="mt-3 space-y-1.5">
        <Field label="Éditeur">{node.publisher}</Field>
        {node.dataset_id !== undefined && <Field label="Jeu de données">{node.dataset_id}</Field>}
        {node.publication_date !== undefined && (
          <Field label="Publié le">{formatDate(node.publication_date)}</Field>
        )}
        {node.retrieved_at !== undefined && (
          <Field label="Récupéré le">{formatDate(node.retrieved_at)}</Field>
        )}
        {node.temporal_scope !== undefined && <Field label="Période">{node.temporal_scope}</Field>}
        {node.geographic_scope !== undefined && (
          <Field label="Périmètre">{node.geographic_scope}</Field>
        )}
        {node.license !== undefined && <Field label="Licence">{node.license}</Field>}
        <Field label="Origine">
          <ExternalAnchor href={node.source_url}>{shortUrl(node.source_url)}</ExternalAnchor>
        </Field>
      </dl>
      <Section title={node.files.length > 1 ? "Copies figées" : "Copie figée"}>
        {node.files.length === 0 ? (
          <p className="font-sans text-[0.8rem] text-ink-3">
            Pas de fichier figé : la source est consultée en ligne (référentiel, texte de loi).
          </p>
        ) : (
          <ul className="space-y-1.5">
            {node.files.map((file) => (
              <FileRow key={file.path} file={file} onOpen={onOpenFile} page={null} />
            ))}
          </ul>
        )}
      </Section>
    </>
  );
}

function shortUrl(url: string): string {
  try {
    const parsed = new URL(url);
    const path = parsed.pathname.length > 40 ? `${parsed.pathname.slice(0, 38)}…` : parsed.pathname;
    return `${parsed.hostname}${path === "/" ? "" : path}`;
  } catch {
    return url;
  }
}

export function DefinitionBody({ node }: { node: DefinitionNode }) {
  return (
    <>
      <blockquote className="mt-3 border-l-2 border-status-definition pl-3 font-serif text-[0.95rem] leading-relaxed text-ink">
        {node.definition}
      </blockquote>
      <dl className="mt-3 space-y-1.5">
        {node.url !== undefined && (
          <Field label="Référence">
            <ExternalAnchor href={node.url}>{shortUrl(node.url)}</ExternalAnchor>
          </Field>
        )}
        {node.last_updated !== undefined && (
          <Field label="Mise à jour">{formatDate(node.last_updated)}</Field>
        )}
      </dl>
      {node.caveats.length > 0 && (
        <Section title="Précautions">
          <ul className="list-disc space-y-1 pl-4 font-sans text-[0.8rem] text-ink-2">
            {node.caveats.map((caveat, i) => (
              <li key={i}>{caveat}</li>
            ))}
          </ul>
        </Section>
      )}
    </>
  );
}

export function HypothesisBody({ node }: { node: HypothesisNode }) {
  const header = (
    <div className="flex items-baseline justify-between">
      <span className="font-mono text-[0.72rem] text-ink-3">{node.name}</span>
      <span className="text-[0.7rem] text-ink-3">
        confiance {CONFIDENCE_LABEL[node.confidence]}
      </span>
    </div>
  );
  // Hypothèse qualitative (directrice, relation) : l'énoncé, sans jauge.
  if (!isQuantifiedHypothesis(node)) {
    return (
      <div className="mt-3 rounded-lg border border-rule bg-white/70 p-3 font-sans">
        {header}
        {node.statement !== undefined && (
          <p className="mt-2 text-[0.85rem] leading-snug text-ink">{node.statement}</p>
        )}
      </div>
    );
  }
  const [low, high] = node.plausible_range;
  const span = high - low;
  const position = span === 0 ? 0.5 : (node.central_value - low) / span;
  return (
    <>
      <div className="mt-3 rounded-lg border border-rule bg-white/70 p-3 font-sans">
        {header}
        <div className="mt-2 flex items-baseline gap-2">
          <span className="text-2xl font-semibold tabular-nums">
            {formatNumber(node.central_value)}
          </span>
          <span className="text-[0.8rem] text-ink-2">{node.unit}</span>
        </div>
        <div className="relative mt-3 h-1.5 rounded-full bg-paper-2">
          <div
            className="absolute inset-y-0 rounded-full"
            style={{
              left: 0,
              right: 0,
              backgroundColor:
                "color-mix(in oklab, var(--color-status-hypothesis) 35%, transparent)",
            }}
          />
          <div
            aria-hidden
            className="absolute -top-1 size-3.5 -translate-x-1/2 rounded-full border-2 border-white bg-status-hypothesis shadow"
            style={{ left: `${Math.max(0, Math.min(1, position)) * 100}%` }}
          />
        </div>
        <div className="mt-1.5 flex justify-between text-[0.7rem] tabular-nums text-ink-3">
          <span>{formatNumber(low)}</span>
          <span>plage plausible</span>
          <span>{formatNumber(high)}</span>
        </div>
      </div>
    </>
  );
}

function LocatorRow({
  locator,
  files,
  onOpenFile,
}: {
  locator: Locator;
  files: ReadonlyArray<EvidenceFile>;
  onOpenFile: OpenFileCommand;
}) {
  const file =
    locator.file === undefined
      ? undefined
      : files.find((candidate) => candidate.path === locator.file);
  const where = [
    locator.page !== undefined ? `p. ${locator.page}` : null,
    locator.sheet !== undefined ? `feuille « ${locator.sheet} »` : null,
    locator.table !== undefined ? locator.table : null,
    locator.section !== undefined
      ? locator.section.startsWith("§")
        ? locator.section
        : `§ ${locator.section}`
      : null,
  ].filter((part) => part !== null);
  return (
    <li className="rounded-md border border-rule bg-white/60 p-2.5">
      {locator.quote !== undefined && (
        <p className="flex gap-2 font-serif text-[0.9rem] leading-relaxed text-ink">
          <Quote aria-hidden className="mt-1 size-3.5 shrink-0 text-status-observation" />
          <span>« {locator.quote} »</span>
        </p>
      )}
      <div className="mt-1.5 flex flex-wrap items-center gap-x-3 gap-y-1 font-sans text-[0.75rem] text-ink-3">
        {file !== undefined ? (
          <button
            type="button"
            disabled={file.hosted === "none"}
            onClick={() => onOpenFile(file, locator.page ?? null)}
            className="inline-flex items-center gap-1 text-status-definition underline decoration-1 underline-offset-2 hover:text-ink disabled:no-underline disabled:opacity-60"
          >
            <FileText aria-hidden className="size-3.5" />
            {file.name}
            {where.length > 0 && `, ${where.join(", ")}`}
          </button>
        ) : (
          where.length > 0 && <span>{where.join(", ")}</span>
        )}
        {locator.url !== undefined && (
          <ExternalAnchor href={locator.url}>{shortUrl(locator.url)}</ExternalAnchor>
        )}
      </div>
    </li>
  );
}

export function ObservationBody({
  node,
  sourceFiles,
  onOpenFile,
}: {
  node: ObservationNode;
  sourceFiles: ReadonlyArray<EvidenceFile>;
  onOpenFile: OpenFileCommand;
}) {
  return (
    <>
      {node.value !== undefined && (
        <p className="mt-3 font-sans text-xl font-semibold tabular-nums text-ink">{node.value}</p>
      )}
      {node.locators.length > 0 && (
        <Section title={node.locators.length > 1 ? "Où le lire" : "Où le lire"}>
          <ul className="space-y-1.5">
            {node.locators.map((locator, i) => (
              <LocatorRow key={i} locator={locator} files={sourceFiles} onOpenFile={onOpenFile} />
            ))}
          </ul>
        </Section>
      )}
    </>
  );
}

export function ComputedBody({
  node,
  onOpenFile,
}: {
  node: ComputedNode;
  onOpenFile: OpenFileCommand;
}) {
  const code: EvidenceFile | null =
    node.produced_by === undefined
      ? null
      : {
          path: node.produced_by.path,
          name: node.produced_by.repo_path,
          mime: "text/x-python; charset=utf-8",
          size: 0,
          hosted: "asset",
        };
  const output: EvidenceFile | null =
    node.output === undefined
      ? null
      : {
          path: node.output.path,
          name: node.output.repo_path,
          mime: "application/json; charset=utf-8",
          size: 0,
          hosted: "asset",
        };
  return (
    <>
      {node.value !== undefined && (
        <p className="mt-3 font-sans text-xl font-semibold tabular-nums text-ink">{node.value}</p>
      )}
      {node.formula !== undefined && (
        <pre className="mt-2 overflow-x-auto rounded-md border border-rule bg-white/70 p-2.5 font-mono text-[0.78rem] leading-relaxed">
          {node.formula}
        </pre>
      )}
      {(code !== null || output !== null) && (
        <Section title="Calcul">
          <ul className="space-y-1.5">
            {code !== null && (
              <li>
                <button
                  type="button"
                  onClick={() => onOpenFile(code, null)}
                  className="flex w-full items-center gap-2 rounded-md border border-rule bg-white/60 px-2.5 py-1.5 text-left font-sans text-[0.8rem] transition-colors hover:border-rule-2 hover:bg-white"
                >
                  <span className="shrink-0 rounded bg-status-transformation px-1 font-mono text-[0.62rem] font-semibold text-white">
                    code
                  </span>
                  <span className="min-w-0 grow truncate font-mono text-[0.75rem]">
                    {code.name}
                  </span>
                </button>
              </li>
            )}
            {output !== null && (
              <li>
                <button
                  type="button"
                  onClick={() => onOpenFile(output, null)}
                  className="flex w-full items-center gap-2 rounded-md border border-rule bg-white/60 px-2.5 py-1.5 text-left font-sans text-[0.8rem] transition-colors hover:border-rule-2 hover:bg-white"
                >
                  <span className="shrink-0 rounded bg-status-result px-1 font-mono text-[0.62rem] font-semibold text-white">
                    sortie
                  </span>
                  <span className="min-w-0 grow truncate font-mono text-[0.75rem]">
                    {output.name}
                  </span>
                </button>
              </li>
            )}
          </ul>
        </Section>
      )}
    </>
  );
}
