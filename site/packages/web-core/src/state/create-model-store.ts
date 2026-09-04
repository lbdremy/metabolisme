import { create, type Draft, type Patches } from "mutative";

/**
 * Snapshot container for external models, enforcing the invariants
 * useSyncExternalStore requires structurally:
 * - the snapshot is an immutable value;
 * - every mutation replaces the snapshot reference (via `update`);
 * - getSnapshot returns the same reference between mutations.
 *
 * Mutative is an implementation detail behind this contract — models depend on
 * ModelStore, never on the engine.
 */
export type ModelStore<Snapshot> = {
  getSnapshot(): Snapshot;
  subscribe(listener: () => void): () => void;
  // Le recipe reçoit un Draft : les champs readonly du snapshot y redeviennent
  // mutables, la mutation ne touchant jamais le snapshot publié lui-même.
  update(recipe: (draft: Draft<Snapshot>) => void): void;
};

export type CreateModelStoreOptions = {
  onPatches?: (patches: Patches, inversePatches: Patches) => void;
};

const isDev = typeof process !== "undefined" && process.env["NODE_ENV"] !== "production";

export function createModelStore<Snapshot extends object>(
  initial: Snapshot,
  options?: CreateModelStoreOptions,
): ModelStore<Snapshot> {
  let snapshot = initial;
  const listeners = new Set<() => void>();

  return {
    getSnapshot() {
      return snapshot;
    },

    subscribe(listener) {
      listeners.add(listener);
      return () => {
        listeners.delete(listener);
      };
    },

    update(recipe) {
      const onPatches = options?.onPatches;
      if (onPatches) {
        const [next, patches, inversePatches] = create(snapshot, recipe, {
          enablePatches: true,
          enableAutoFreeze: isDev,
        });
        // Immutable<Snapshot> → Snapshot : l'immutabilité est le contrat du
        // store ; les types de snapshot des modèles sont déclarés readonly.
        snapshot = next as Snapshot;
        onPatches(patches, inversePatches);
      } else {
        snapshot = create(snapshot, recipe, {
          enableAutoFreeze: isDev,
        }) as Snapshot;
      }
      for (const listener of listeners) {
        listener();
      }
    },
  };
}
