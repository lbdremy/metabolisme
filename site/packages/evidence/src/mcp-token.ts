import { deriveNoteToken } from "./note-token.ts";

// Jeton de l'adresse du serveur MCP : même dérivation que les notes, sur une
// étiquette qu'aucun slug ne peut prendre (les slugs n'ont pas de « : »).
// L'adresse est donc secrète comme celles des notes, sans secret de plus à
// gérer. Pour la révoquer sans toucher aux notes : incrémenter la version.
export const MCP_TOKEN_LABEL = "mcp:v1";

export function deriveMcpToken(secret: string): Promise<string> {
  return deriveNoteToken(secret, MCP_TOKEN_LABEL);
}

// Comparaison en temps constant : le jeton est la seule protection.
export function tokensMatch(expected: string, received: string): boolean {
  if (expected.length !== received.length) return false;
  let difference = 0;
  for (let i = 0; i < expected.length; i += 1) {
    difference |= expected.charCodeAt(i) ^ received.charCodeAt(i);
  }
  return difference === 0;
}
