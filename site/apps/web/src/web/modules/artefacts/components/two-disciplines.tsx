import { Link } from "@tanstack/react-router";
import { ARTEFACT_KINDS, type ArtefactKind } from "../model/artefact-kind";
import { ArtefactKindBadge } from "./artefact-kind-badge";

const ORDER: ReadonlyArray<{ kind: ArtefactKind; anchor: string }> = [
  { kind: "research", anchor: "#recherche" },
  { kind: "design", anchor: "#conception" },
];

// Les deux types d'articles côte à côte, sur l'accueil : ce qu'ils
// demandent, ce qui les porte, et ce qui les relie.
export function TwoDisciplines() {
  return (
    <section aria-labelledby="deux-types" className="border-b border-rule py-10">
      <h2
        id="deux-types"
        className="font-sans text-[0.75rem] font-semibold uppercase tracking-wider text-ink-3"
      >
        Deux types d'articles
      </h2>
      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        {ORDER.map(({ kind, anchor }) => {
          const info = ARTEFACT_KINDS[kind];
          return (
            <a
              key={kind}
              href={anchor}
              className="group block rounded-lg border border-rule bg-white/60 p-5 hover:border-rule-2"
              style={{ borderTopColor: info.color, borderTopWidth: 3 }}
            >
              <ArtefactKindBadge kind={kind} />
              <p className="mt-3 font-sans text-[1.1rem] font-bold leading-snug text-ink group-hover:underline group-hover:decoration-2 group-hover:underline-offset-4">
                {info.discipline}
              </p>
              <p className="mt-2 font-serif text-[0.98rem] italic leading-relaxed text-ink-2">
                {info.question}
              </p>
              <p className="mt-2 font-serif text-[0.95rem] leading-relaxed text-ink-2">
                {info.carries}
              </p>
            </a>
          );
        })}
      </div>
      <p className="mt-5 max-w-[62ch] font-serif text-[1rem] leading-relaxed text-ink-2">
        Les deux partagent la même chaîne de preuves. Un article de conception s'appuie sur des
        faits établis, parfois sur des nœuds d'un article de recherche ; chacune de ses limites est
        une question que la recherche peut instruire.{" "}
        <Link to="/methode" className="text-ink underline decoration-1 underline-offset-2">
          La méthode
        </Link>{" "}
        les distingue et dit comment l'une nourrit l'autre.
      </p>
    </section>
  );
}
