import { Link } from "@tanstack/react-router";
import { ArrowRight } from "lucide-react";
import type { Post } from "~/contracts/evidence";
import { formatDate } from "~/web/modules/evidence/model/format";

export function PostList({ posts }: { posts: ReadonlyArray<Post> }) {
  return (
    <ul className="divide-y divide-rule">
      {posts.map((post) => (
        <li key={post.slug} className="py-7 first:pt-0">
          <Link to="/posts/$slug" params={{ slug: post.slug }} className="group block">
            <p className="font-sans text-[0.72rem] font-semibold uppercase tracking-wider text-ink-3">
              {post.study.name} · {formatDate(post.date)}
            </p>
            <h2 className="mt-2 font-sans text-[1.5rem] font-bold leading-tight tracking-tight text-ink group-hover:underline group-hover:decoration-2 group-hover:underline-offset-4">
              {post.title}
            </h2>
            {post.subtitle !== undefined && (
              <p className="mt-1.5 font-serif text-[1.05rem] text-ink-2">{post.subtitle}</p>
            )}
            {post.summary !== undefined && (
              <p className="mt-3 font-serif text-[0.95rem] leading-relaxed text-ink-2">
                {post.summary.trim()}
              </p>
            )}
            <span className="mt-3 inline-flex items-center gap-1 font-sans text-[0.8rem] font-medium text-ink">
              Lire, avec la chaîne de preuves
              <ArrowRight
                aria-hidden
                className="size-3.5 transition-transform group-hover:translate-x-0.5"
              />
            </span>
          </Link>
        </li>
      ))}
    </ul>
  );
}
