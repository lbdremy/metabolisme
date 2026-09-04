/**
 * Memoizes a pure snapshot → ViewModel projection per snapshot reference:
 * same snapshot reference → same ViewModel reference. Without this, a fresh
 * ViewModel per render silently defeats React.memo children and makes
 * useEffect dependencies on ViewModel fields unreliable.
 */
export function memoProjection<Snapshot extends object, ViewModel>(
  project: (snapshot: Snapshot) => ViewModel,
): (snapshot: Snapshot) => ViewModel {
  const cache = new WeakMap<Snapshot, ViewModel>();

  return (snapshot) => {
    if (cache.has(snapshot)) {
      return cache.get(snapshot) as ViewModel;
    }
    const viewModel = project(snapshot);
    cache.set(snapshot, viewModel);
    return viewModel;
  };
}
