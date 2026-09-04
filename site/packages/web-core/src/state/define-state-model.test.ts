import { describe, expect, it } from "vitest";
import { assertNever } from "./assert-never.ts";
import { defineStateModel } from "./define-state-model.ts";

type PlayerState = { status: "paused" } | { status: "playing" };

type PlayerEvent = { type: "play" } | { type: "pause" };

type PlayerEffect = { kind: "start-audio" } | { kind: "stop-audio" };

const playerModel = defineStateModel<PlayerState, PlayerEvent, PlayerEffect>({
  initial: { status: "paused" },
  transition(state, event) {
    switch (state.status) {
      case "paused":
        switch (event.type) {
          case "play":
            return {
              disposition: { kind: "handled" },
              nextState: { status: "playing" },
              effects: [{ kind: "start-audio" }],
            };
          case "pause":
            return {
              disposition: { kind: "ignored", reason: "already paused" },
              nextState: state,
              effects: [],
            };
          default:
            return assertNever(event);
        }
      case "playing":
        switch (event.type) {
          case "pause":
            return {
              disposition: { kind: "handled" },
              nextState: { status: "paused" },
              effects: [{ kind: "stop-audio" }],
            };
          case "play":
            return {
              disposition: { kind: "ignored", reason: "already playing" },
              nextState: state,
              effects: [],
            };
          default:
            return assertNever(event);
        }
      default:
        return assertNever(state);
    }
  },
});

describe("defineStateModel", () => {
  it("handles a valid transition with effects", () => {
    const result = playerModel.transition(playerModel.initial, {
      type: "play",
    });
    expect(result.disposition.kind).toBe("handled");
    expect(result.nextState.status).toBe("playing");
    expect(result.effects).toEqual([{ kind: "start-audio" }]);
  });

  it("classifies an irrelevant event with an explicit disposition", () => {
    const result = playerModel.transition(playerModel.initial, {
      type: "pause",
    });
    expect(result.disposition).toEqual({
      kind: "ignored",
      reason: "already paused",
    });
    expect(result.nextState).toBe(playerModel.initial);
    expect(result.effects).toEqual([]);
  });
});
