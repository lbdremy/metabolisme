// Module virtuel produit au build par vite-plugins/content-assets.
declare module "virtual:content-index" {
  export const contentIndex: {
    readonly posts: readonly {
      readonly slug: string;
      readonly post: unknown;
      readonly markdown: string;
    }[];
    readonly notes: readonly {
      readonly token: string;
      readonly note: unknown;
      readonly markdown: string;
    }[];
    readonly pages: readonly { readonly slug: string; readonly markdown: string }[];
  };
}
