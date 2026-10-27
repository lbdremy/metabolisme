import { createFileRoute, redirect } from "@tanstack/react-router";

// L'ancien sommaire « Livret 2027 » : ses articles sont devenus les articles
// de conception. L'adresse a été partagée avec ceux qui relisent ; elle mène
// au sommaire de la conception, relecture comprise.
export const Route = createFileRoute("/livret")({
  beforeLoad: () => {
    throw redirect({ to: "/conception", search: { relecture: true }, statusCode: 301 });
  },
});
