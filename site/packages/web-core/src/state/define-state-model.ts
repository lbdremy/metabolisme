/**
 * Explicit state machines: every (state × event) cell must classify the event
 * with a disposition. Silent fall-through is forbidden — the double assertNever
 * (inner event switch, outer state switch) proves the matrix is exhaustive.
 *
 * Effects are descriptions, not executions: the model returns what should
 * happen, an outer runtime performs it and feeds the outcome back as an event.
 */
export type Disposition =
  | { kind: "handled" }
  | { kind: "ignored"; reason: string }
  | { kind: "stale"; reason: string }
  | { kind: "deferred"; reason: string }
  | { kind: "superseded"; reason: string }
  | { kind: "rejected"; reason: string }
  | { kind: "unexpected"; reason: string };

export type TransitionResult<State, Effect> = {
  disposition: Disposition;
  nextState: State;
  effects: ReadonlyArray<Effect>;
};

export type StateModel<State, Event, Effect> = {
  initial: State;
  transition: (state: State, event: Event) => TransitionResult<State, Effect>;
};

export function defineStateModel<State, Event, Effect = never>(
  model: StateModel<State, Event, Effect>,
): StateModel<State, Event, Effect> {
  return model;
}
