import { createFileRoute, redirect } from "@tanstack/react-router";
import { z } from "zod";
import {
  conceptionSlug,
  isConception,
  isPublishedConception,
  NODE_ID_PATTERN,
} from "~/contracts/evidence";
import { NoteHeader } from "~/web/modules/notes/components/note-header";
import { ReadingLayout } from "~/web/modules/reading/components/reading-layout";
import { getNote } from "~/web-rpc/public";

const SearchSchema = z.object({
  n: z.string().regex(NODE_ID_PATTERN).optional().catch(undefined),
});

// Une note n'est accessible que par son jeton : ni listée ni indexée. Un
// article de conception en relecture aussi. Une fois PUBLIÉ (note.yaml,
// `status: published`), il a une adresse lisible et durable, et son jeton
// y redirige (301), nœud ouvert compris : les liens déjà partagés suivent.
export const Route = createFileRoute("/notes/$token")({
  validateSearch: SearchSchema,
  loader: async ({ params, location }) => {
    const entry = await getNote({ data: { token: params.token } });
    if (isPublishedConception(entry.note)) {
      // Le nœud ouvert se lit dans l'URL sans devenir une dépendance du
      // chargeur : ouvrir un nœud ne refait pas la requête.
      const { n } = SearchSchema.parse(location.search);
      throw redirect({
        to: "/conception/$slug",
        params: { slug: conceptionSlug(entry.note) },
        search: n === undefined ? {} : { n },
        statusCode: 301,
      });
    }
    return entry;
  },
  head: ({ loaderData }) => ({
    meta: [
      { name: "robots", content: "noindex, nofollow" },
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
