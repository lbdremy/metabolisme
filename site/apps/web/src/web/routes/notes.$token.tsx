import { createFileRoute } from "@tanstack/react-router";
import { z } from "zod";
import { isConception, isPublishedConception, NODE_ID_PATTERN } from "~/contracts/evidence";
import { NoteHeader } from "~/web/modules/notes/components/note-header";
import { ReadingLayout } from "~/web/modules/reading/components/reading-layout";
import { getNote } from "~/web-rpc/public";

const SearchSchema = z.object({
  n: z.string().regex(NODE_ID_PATTERN).optional().catch(undefined),
});

// Une note n'est accessible que par son jeton. Une note isolée n'est ni
// listée ni indexée ; un article de conception l'est quand il est publié
// (note.yaml, `status: published`), et reste hors index en relecture. La page
// reste publique pour qui a le lien.
export const Route = createFileRoute("/notes/$token")({
  validateSearch: SearchSchema,
  loader: ({ params }) => getNote({ data: { token: params.token } }),
  head: ({ loaderData }) => ({
    meta: [
      ...(loaderData !== undefined && isPublishedConception(loaderData.note)
        ? []
        : [{ name: "robots", content: "noindex, nofollow" }]),
      ...(loaderData === undefined
        ? []
        : [
            {
              title: `${loaderData.note.title} — ${isConception(loaderData.note) ? "conception" : "note"} Métabolisme`,
            },
          ]),
    ],
  }),
  component: NotePage,
});

function NotePage() {
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
      kindLabel={isConception(note) ? "article de conception" : "note partagée par lien"}
    />
  );
}
