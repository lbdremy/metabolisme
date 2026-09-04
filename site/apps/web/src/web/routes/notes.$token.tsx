import { createFileRoute } from "@tanstack/react-router";
import { z } from "zod";
import { NODE_ID_PATTERN } from "~/contracts/evidence";
import { NoteHeader } from "~/web/modules/notes/components/note-header";
import { ReadingLayout } from "~/web/modules/reading/components/reading-layout";
import { getNote } from "~/web-rpc/public";

const SearchSchema = z.object({
  n: z.string().regex(NODE_ID_PATTERN).optional().catch(undefined),
});

// Une note n'est accessible que par son jeton ; elle n'est ni listée ni
// indexée. La page reste publique pour qui a le lien.
export const Route = createFileRoute("/notes/$token")({
  validateSearch: SearchSchema,
  loader: ({ params }) => getNote({ data: { token: params.token } }),
  head: ({ loaderData }) => ({
    meta: [
      { name: "robots", content: "noindex, nofollow" },
      ...(loaderData === undefined
        ? []
        : [{ title: `${loaderData.note.title} — note Métabolisme` }]),
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
      robotsNoIndex
    />
  );
}
