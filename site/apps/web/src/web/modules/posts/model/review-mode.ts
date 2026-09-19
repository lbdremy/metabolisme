// Le mode relecture : les posts « en attente de relecture » (statut
// in_review) sont en ligne à leur adresse mais absents de l'index. Le lecteur
// qui relit les réaffiche par un geste discret — trois clics rapprochés sur
// le logo du pied de page. Ce n'est pas une protection (l'adresse suffit
// déjà) : c'est un interrupteur qui ne s'offre pas au passant.
//
// Ici, la partie pure : la reconnaissance du geste. Le stockage et l'horloge
// vivent dans le hook.

export const REVIEW_MODE_TAPS = 3;
export const REVIEW_MODE_WINDOW_MS = 1000;

// Les clics déjà comptés dans la fenêtre courante.
export type TapSequence = { readonly count: number; readonly lastAt: number };

export const NO_TAPS: TapSequence = { count: 0, lastAt: 0 };

export type TapResult = { readonly sequence: TapSequence; readonly completed: boolean };

// Un clic de trop tard rouvre une séquence plutôt que de la casser : le
// quatrième clic d'une série lente est le premier d'une nouvelle.
export function registerTap(sequence: TapSequence, at: number): TapResult {
  const continues = sequence.count > 0 && at - sequence.lastAt <= REVIEW_MODE_WINDOW_MS;
  const count = (continues ? sequence.count : 0) + 1;
  return count >= REVIEW_MODE_TAPS
    ? { sequence: NO_TAPS, completed: true }
    : { sequence: { count, lastAt: at }, completed: false };
}
