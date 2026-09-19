import { describe, expect, it } from "vitest";
import { NO_TAPS, registerTap, REVIEW_MODE_WINDOW_MS } from "./review-mode";

function tap(times: ReadonlyArray<number>): ReadonlyArray<boolean> {
  let sequence = NO_TAPS;
  return times.map((at) => {
    const result = registerTap(sequence, at);
    sequence = result.sequence;
    return result.completed;
  });
}

describe("registerTap", () => {
  it("completes on the third tap inside the window", () => {
    expect(tap([0, 200, 400])).toEqual([false, false, true]);
  });

  it("never completes when the taps are too far apart", () => {
    const slow = REVIEW_MODE_WINDOW_MS + 1;
    expect(tap([0, slow, 2 * slow, 3 * slow])).toEqual([false, false, false, false]);
  });

  it("starts a new sequence after a late tap", () => {
    expect(tap([0, 200, 200 + REVIEW_MODE_WINDOW_MS + 1, 300 + REVIEW_MODE_WINDOW_MS + 1])).toEqual(
      [false, false, false, false],
    );
  });

  it("restarts counting after a completed gesture", () => {
    expect(tap([0, 100, 200, 300, 400, 500])).toEqual([false, false, true, false, false, true]);
  });
});
