// Dérivation du jeton public d'une note : HMAC-SHA-256(secret, slug), rendu en
// base 36 sur 24 caractères (~124 bits). Même slug + même secret → même URL,
// donc une note republiée garde son adresse ; sans le secret, le slug ne
// permet pas de deviner l'adresse. Implémentée avec WebCrypto pour tourner
// au build (Node) comme dans un Worker.

const TOKEN_LENGTH = 24;

export async function deriveNoteToken(secret: string, slug: string): Promise<string> {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const digest = new Uint8Array(
    await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(slug)),
  );
  // 32 octets → grand entier → base 36, tronqué : suffisant et lisible.
  let value = 0n;
  for (const byte of digest) value = (value << 8n) | BigInt(byte);
  return value.toString(36).padStart(TOKEN_LENGTH, "0").slice(0, TOKEN_LENGTH);
}
