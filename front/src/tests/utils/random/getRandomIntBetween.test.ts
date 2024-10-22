import { describe, expect, test } from "vitest";
import { getRandomIntBetween } from "$lib/utils/random";

function toPercent(value: number, total: number): number {
  return Math.floor((value / total) * 100);
}

describe("getRandomIntBetween", () => {
  test("should distribute random values equally", () => {
    const count = {
      "1": 0,
      "2": 0,
      "3": 0,
    };

    const iterNumber = 20000000;
    for (let i = 0; i < iterNumber; i++) {
      count[getRandomIntBetween(1, 3)]++;
    }

    // Note: les assertions gère le cas - à la marge - où la répartition n'est pas exactement égale
    expect(toPercent(count["1"], iterNumber)).toBeGreaterThanOrEqual(32);
    expect(toPercent(count["1"], iterNumber)).toBeLessThanOrEqual(34);

    expect(toPercent(count["2"], iterNumber)).toBeGreaterThanOrEqual(32);
    expect(toPercent(count["2"], iterNumber)).toBeLessThanOrEqual(34);

    expect(toPercent(count["3"], iterNumber)).toBeGreaterThanOrEqual(32);
    expect(toPercent(count["3"], iterNumber)).toBeLessThanOrEqual(34);
  });
});
