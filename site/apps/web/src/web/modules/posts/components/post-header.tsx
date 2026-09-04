import { ExternalLink, Tag } from "lucide-react";
import type { Post } from "~/contracts/evidence";
import { formatDate } from "~/web/modules/evidence/model/format";

// En-tête d'un post : titre, sous-titre, étude, date et version du
// raisonnement (tag Git) — l'article est rattaché à une version précise.
export function PostHeader({ post }: { post: Post }) {
  return (
    <header>
      <p className="font-sans text-[0.75rem] font-semibold uppercase tracking-wider text-ink-3">
        {post.study.name} · {formatDate(post.date)}
      </p>
      <h1 className="mt-3 font-sans text-[2rem] font-bold leading-[1.12] tracking-tight text-ink sm:text-[2.4rem]">
        {post.title}
      </h1>
      {post.subtitle !== undefined && (
        <p className="mt-3 font-serif text-[1.2rem] leading-snug text-ink-2">{post.subtitle}</p>
      )}
      {post.study.question !== undefined && (
        <blockquote className="mt-5 border-l-2 border-rule-2 pl-4 font-serif text-[0.95rem] italic leading-relaxed text-ink-2">
          {post.study.question.trim()}
        </blockquote>
      )}
      <VersionLine version={post.version} />
    </header>
  );
}

export function VersionLine({ version }: { version: Post["version"] }) {
  if (version.tag === undefined && version.commit === undefined) return null;
  const ref = version.tag ?? version.commit ?? "";
  const href =
    version.repo_url === undefined
      ? null
      : `${version.repo_url}/tree/${encodeURIComponent(ref)}${version.evidence_doc === undefined ? "" : `/${version.evidence_doc}`}`;
  return (
    <p className="mt-4 inline-flex flex-wrap items-center gap-x-2 gap-y-1 rounded-full border border-rule bg-white/60 px-3 py-1 font-sans text-[0.75rem] text-ink-2">
      <Tag aria-hidden className="size-3.5 text-ink-3" />
      version du raisonnement <span className="font-mono">{ref}</span>
      {href !== null && (
        <a
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 underline decoration-1 underline-offset-2 hover:text-ink"
        >
          dépôt <ExternalLink aria-hidden className="size-3" />
        </a>
      )}
    </p>
  );
}
