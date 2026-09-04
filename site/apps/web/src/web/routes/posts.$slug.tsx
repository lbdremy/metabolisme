import { createFileRoute } from "@tanstack/react-router";
import { z } from "zod";
import { NODE_ID_PATTERN } from "~/contracts/evidence";
import { PostHeader } from "~/web/modules/posts/components/post-header";
import { ReadingLayout } from "~/web/modules/reading/components/reading-layout";
import { getPost } from "~/web-rpc/public";

// Le nœud ouvert dans le panneau est un état d'URL (?n=R-07) : partageable,
// validé à la frontière de route.
const SearchSchema = z.object({
  n: z.string().regex(NODE_ID_PATTERN).optional().catch(undefined),
});

export const Route = createFileRoute("/posts/$slug")({
  validateSearch: SearchSchema,
  loader: ({ params }) => getPost({ data: { slug: params.slug } }),
  head: ({ loaderData }) => ({
    meta:
      loaderData === undefined
        ? []
        : [
            { title: `${loaderData.post.title} — Métabolisme` },
            ...(loaderData.post.summary === undefined
              ? []
              : [{ name: "description", content: loaderData.post.summary.trim() }]),
          ],
  }),
  component: PostPage,
});

function PostPage() {
  const { post, markdown } = Route.useLoaderData();
  const { n } = Route.useSearch();
  const navigate = Route.useNavigate();

  return (
    <ReadingLayout
      key={post.slug}
      publication={{ kind: "posts", id: post.slug }}
      header={<PostHeader post={post} />}
      markdown={markdown}
      selectedId={n ?? null}
      onNavigate={(id) => {
        void navigate({
          search: id === null ? {} : { n: id },
          replace: true,
          resetScroll: false,
        });
      }}
    />
  );
}
