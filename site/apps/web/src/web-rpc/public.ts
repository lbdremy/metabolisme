// Surface RPC curée : seul point d'entrée que web/ a le droit d'importer.
export {
  getNote,
  getPage,
  getPost,
  listCollection,
  listPosts,
  listPostsInReview,
} from "./publications.functions";
