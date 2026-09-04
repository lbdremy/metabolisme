// Surface curée du contenu statique : seul point d'entrée que web/ a le droit
// d'importer, sur le modèle de web-rpc/public.ts.
export {
  contentFileUrl,
  fetchGraph,
  fetchMarkdown,
  type PublicationRef,
} from "./publications.assets";
