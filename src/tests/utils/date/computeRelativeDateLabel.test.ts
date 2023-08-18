import { computeRelativeDateLabel } from "$lib/components/display/relative-date-label.svelte";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";

describe("computeUpdateStatus et computeRelativeDateLabel", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });
  afterEach(() => {
    vi.useRealTimers();
  });

  test("moins d'un jour", () => {
    // ÉTANT DONNÉ la date du 1er janvier à 13h
    const startDate = new Date(2022, 1, 1, 13);

    // ET que nous sommes le 1er janvier à 14h
    const date = new Date(2022, 1, 1, 14);
    vi.setSystemTime(date);

    // ALORS la réponse est "aujourd’hui"
    expect(computeRelativeDateLabel(startDate)).toStrictEqual("aujourd’hui");
  });

  test("moins d'une semaine", () => {
    // ÉTANT DONNÉ la date du 1er janvier à 13h
    const startDate = new Date(2022, 1, 1, 13);

    // ET que nous sommes le 6 janvier à 14h
    const date = new Date(2022, 1, 6, 14);
    vi.setSystemTime(date);

    // ALORS la réponse est "il y a 5 jours"
    expect(computeRelativeDateLabel(startDate)).toStrictEqual("il y a 5 jours");
  });

  test("moins de deux semaines", () => {
    // ÉTANT DONNÉ la date du 1er janvier à 13h
    const startDate = new Date(2022, 1, 1, 13);

    // ET que nous sommes le 13 janvier à 14h
    const date = new Date(2022, 1, 13, 14);
    vi.setSystemTime(date);

    // ALORS la réponse est "il y a 1 semaine"
    expect(computeRelativeDateLabel(startDate)).toStrictEqual(
      "il y a 1 semaine"
    );
  });

  test("moins d'un mois", () => {
    // ÉTANT DONNÉ la date du 1er janvier à 13h
    const startDate = new Date(2022, 1, 1, 13);

    // ET que nous sommes le 28 janvier à 14h
    const date = new Date(2022, 1, 28, 14);
    vi.setSystemTime(date);

    // ALORS la réponse est "il y a 3 semaines"
    expect(computeRelativeDateLabel(startDate)).toStrictEqual(
      "il y a 3 semaines"
    );
  });

  test("plus d'un mois", () => {
    // ÉTANT DONNÉ la date du 1er janvier à 13h
    const startDate = new Date(2022, 1, 1, 13);

    // ET que nous sommes le 10 février à 14h
    const date = new Date(2022, 2, 10, 14);
    vi.setSystemTime(date);

    // ALORS pas d'actualisation nécessaire et la réponse est il y a 5 semaines
    expect(computeRelativeDateLabel(startDate)).toStrictEqual(
      "il y a 5 semaines"
    );
  });

  test("plus de 3 mois", () => {
    // ÉTANT DONNÉ la date du 1er janvier à 13h
    const startDate = new Date(2022, 1, 1, 13);

    // ET que nous sommes le 10 avril à 14h
    const date = new Date(2022, 4, 10, 14);
    vi.setSystemTime(date);

    // ALORS la réponse est il y a 3 mois
    expect(computeRelativeDateLabel(startDate)).toStrictEqual("il y a 3 mois");
  });

  test("plus de 6 mois", () => {
    // ÉTANT DONNÉ la date du 1er janvier à 13h
    const startDate = new Date(2022, 1, 1, 13);

    // ET que nous sommes le 10 juillet à 14h
    const date = new Date(2022, 7, 10, 14);
    vi.setSystemTime(date);

    // ALORS la réponse est "il y a 6 mois"
    expect(computeRelativeDateLabel(startDate)).toStrictEqual("il y a 6 mois");
  });

  test("plus de 10 mois", () => {
    // ÉTANT DONNÉ la date du 1er janvier à 13h
    const startDate = new Date(2022, 1, 1, 13);

    // ET que nous sommes le 10 octobre à 14h
    const date = new Date(2022, 10, 10, 14);
    vi.setSystemTime(date);

    // ALORS la réponse est "il y a 9 mois"
    expect(computeRelativeDateLabel(startDate)).toStrictEqual("il y a 9 mois");
  });

  test("plus de 2 ans", () => {
    // ÉTANT DONNÉ la date du 1er janvier à 13h
    const startDate = new Date(2022, 1, 1, 13);

    // ET que nous sommes le 1 janvier 2024
    const date = new Date(2024, 1, 1, 14);
    vi.setSystemTime(date);

    // ALORS la réponse est "il y a plus de 2 ans"
    expect(computeRelativeDateLabel(startDate)).toStrictEqual(
      "il y a plus de 2 ans"
    );
  });
});
