import { createFileRoute } from "@tanstack/react-router";
import { z } from "zod";
import { NODE_ID_PATTERN } from "~/contracts/evidence";
import { NoteHeader } from "~/web/modules/notes/components/note-header";
import { ReadingLayout } from "~/web/modules/reading/components/reading-layout";
import { getConceptionArticle } from "~/web-rpc/public";

const SearchSchema = z.object({
  n: z.string().regex(NODE_ID_PATTERN).optional().catch(undefined),
});

// Un article de conception publié, à son adresse lisible et durable. Le
// contenu (graphe, fichiers) reste rangé sous son jeton : seule l'adresse de
// lecture change quand l'article passe de la relecture à la publication.
export const Route = createFileRoute("/conception_/$slug")({
  validateSearch: SearchSchema,
  loader: ({ params }) => getConceptionArticle({ data: { slug: params.slug } }),
  head: ({ loaderData }) => ({
    meta:
      loaderData === undefined
        ? []
        : [
            { title: `${loaderData.note.title} — conception Métabolisme` },
            ...(loaderData.note.context === undefined
              ? []
              : [{ name: "description", content: loaderData.note.context.trim() }]),
          ],
  }),
  component: ConceptionArticlePage,
});

function ConceptionArticlePage() {
  const { token, note, markdown } = Route.useLoaderData();
  const { n } = Route.useSearch();
  const navigate = Route.useNavigate();

  return (
    <ReadingLayout
      key={token}
      publication={{ kind: "notes", id: token }}
      header={<NoteHeader note={note} />}
      markdown={markdown}
      selectedId={n ?? null}
      onNavigate={(id) => {
        void navigate({
          search: id === null ? {} : { n: id },
          replace: true,
          resetScroll: false,
        });
      }}
      kindLabel="article de conception"
    />
  );
}
