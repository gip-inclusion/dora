import type { Service } from "$lib/types";
import {
  computeUpdateStatusData,
  computeUpdateStatusLabel,
} from "$lib/utils/service";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";

describe("computeUpdateStatusData et computeUpdateStatusDataLabel", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });
  afterEach(() => {
    vi.useRealTimers();
  });

  test("moins d'un jour", () => {
    // ÉTANT DONNÉ un service publié et modifié à 13h
    const service = {
      modificationDate: new Date(2022, 1, 1, 13),
      status: "PUBLISHED",
    } as unknown as Service;

    // SI je récupère ses données d'actualisation le même jour à 14h
    const date = new Date(2022, 1, 1, 14);
    vi.setSystemTime(date);
    const res = computeUpdateStatusData(service);
    const label = computeUpdateStatusLabel({ ...res });

    // ALORS pas d'actualisation nécessaire et il est considéré comme actualisé aujourd'hui
    expect(res).toStrictEqual({
      dayDiff: 0,
      weekDiff: 0,
      monthDiff: 0,
      yearDiff: 0,
      updateStatus: "NOT_NEEDED",
    });
    expect(label).toStrictEqual("Actualisé aujourd'hui");
  });

  test("moins d'une semaine", () => {
    // ÉTANT DONNÉ un service publié et modifié le 1er janvier à 13h
    const service = {
      modificationDate: new Date(2022, 1, 1, 13),
      status: "PUBLISHED",
    } as unknown as Service;

    // SI je récupère ses données d'actualisation le 6 janvier à 14h
    const date = new Date(2022, 1, 6, 14);
    vi.setSystemTime(date);

    const res = computeUpdateStatusData(service);
    const label = computeUpdateStatusLabel({ ...res });

    // ALORS pas d'actualisation nécessaire et il est considéré comme actualisé il y a 5 jours
    expect(res).toStrictEqual({
      dayDiff: 5,
      weekDiff: 0,
      monthDiff: 0,
      yearDiff: 0,
      updateStatus: "NOT_NEEDED",
    });
    expect(label).toStrictEqual("Actualisé il y a 5 jours");
  });

  test("moins de deux semaines", () => {
    // ÉTANT DONNÉ un service publié et modifié le 1er janvier à 13h
    const service = {
      modificationDate: new Date(2022, 1, 1, 13),
      status: "PUBLISHED",
    } as unknown as Service;

    // SI je récupère ses données d'actualisation le 13 janvier à 14h
    const date = new Date(2022, 1, 13, 14);
    vi.setSystemTime(date);

    const res = computeUpdateStatusData(service);
    const label = computeUpdateStatusLabel({ ...res });

    // ALORS pas d'actualisation nécessaire et il est considéré comme actualisé il y a 1 semaine
    expect(res).toStrictEqual({
      dayDiff: 12,
      weekDiff: 1,
      monthDiff: 0,
      yearDiff: 0,
      updateStatus: "NOT_NEEDED",
    });
    expect(label).toStrictEqual("Actualisé il y a 1 semaine");
  });
  test("moins d'un mois", () => {
    // ÉTANT DONNÉ un service publié et modifié le 1er janvier à 13h
    const service = {
      modificationDate: new Date(2022, 1, 1, 13),
      status: "PUBLISHED",
    } as unknown as Service;

    // SI je récupère ses données d'actualisation le 28 janvier à 14h
    const date = new Date(2022, 1, 28, 14);
    vi.setSystemTime(date);

    const res = computeUpdateStatusData(service);
    const label = computeUpdateStatusLabel({ ...res });

    // ALORS pas d'actualisation nécessaire et il est considéré comme actualisé il y a 5 jours
    expect(res).toStrictEqual({
      dayDiff: 27,
      weekDiff: 3,
      monthDiff: 0,
      yearDiff: 0,
      updateStatus: "NOT_NEEDED",
    });
    expect(label).toStrictEqual("Actualisé il y a 3 semaines");
  });

  test("plus d'un mois", () => {
    // ÉTANT DONNÉ un service publié et modifié le 1er janvier à 13h
    const service = {
      modificationDate: new Date(2022, 1, 1, 13),
      status: "PUBLISHED",
    } as unknown as Service;

    // SI je récupère ses données d'actualisation le 10 février à 14h
    const date = new Date(2022, 2, 10, 14);
    vi.setSystemTime(date);

    const res = computeUpdateStatusData(service);
    const label = computeUpdateStatusLabel({ ...res });

    // ALORS pas d'actualisation nécessaire et il est considéré comme actualisé il y a 5 semaines
    expect(res).toStrictEqual({
      dayDiff: 37,
      weekDiff: 5,
      monthDiff: 1,
      yearDiff: 0,
      updateStatus: "NOT_NEEDED",
    });
    expect(label).toStrictEqual("Actualisé il y a 5 semaines");
  });

  test("plus de 3 mois", () => {
    // ÉTANT DONNÉ un service publié et modifié le 1er janvier à 13h
    const service = {
      modificationDate: new Date(2022, 1, 1, 13),
      status: "PUBLISHED",
    } as unknown as Service;

    // SI je récupère ses données d'actualisation le 10 avril à 14h
    const date = new Date(2022, 4, 10, 14);
    vi.setSystemTime(date);

    const res = computeUpdateStatusData(service);
    const label = computeUpdateStatusLabel({ ...res });

    // ALORS pas d'actualisation nécessaire et il est considéré comme actualisé il y a 3 mois
    expect(res).toStrictEqual({
      dayDiff: 98,
      weekDiff: 14,
      monthDiff: 3,
      yearDiff: 0,
      updateStatus: "NOT_NEEDED",
    });
    expect(label).toStrictEqual("Actualisé il y a 3 mois");
  });

  test("plus de 6 mois et service publié", () => {
    // ÉTANT DONNÉ un service publié et modifié le 1er janvier à 13h
    const service = {
      modificationDate: new Date(2022, 1, 1, 13),
      status: "PUBLISHED",
    } as unknown as Service;

    // SI je récupère ses données d'actualisation le 10 juillet à 14h
    const date = new Date(2022, 7, 10, 14);
    vi.setSystemTime(date);

    const res = computeUpdateStatusData(service);
    const label = computeUpdateStatusLabel({ ...res });

    // ALORS l'actualisation est demandée et il est considéré comme actualisé il y a 10 mois
    expect(res).toStrictEqual({
      dayDiff: 190,
      weekDiff: 27,
      monthDiff: 6,
      yearDiff: 0,
      updateStatus: "NEEDED",
    });
    expect(label).toStrictEqual("Actualisé il y a 6 mois");
  });

  test("plus de 6 mois et service en brouillon", () => {
    // ÉTANT DONNÉ un service en brouillon et modifié le 1er janvier à 13h
    const service = {
      modificationDate: new Date(2022, 1, 1, 13),
      status: "DRAFT",
    } as unknown as Service;

    // SI je récupère ses données d'actualisation le 10 juillet à 14h
    const date = new Date(2022, 7, 10, 14);
    vi.setSystemTime(date);

    const res = computeUpdateStatusData(service);
    const label = computeUpdateStatusLabel({ ...res });

    // ALORS l'actualisation n'est demandée
    expect(res).toStrictEqual({
      dayDiff: 190,
      weekDiff: 27,
      monthDiff: 6,
      yearDiff: 0,
      updateStatus: "NOT_NEEDED",
    });
    expect(label).toStrictEqual("Actualisé il y a 6 mois");
  });

  test("plus de 10 mois et service publié", () => {
    // ÉTANT DONNÉ un service publié et modifié le 1er janvier à 13h
    const service = {
      modificationDate: new Date(2022, 1, 1, 13),
      status: "PUBLISHED",
    } as unknown as Service;

    // SI je récupère ses données d'actualisation le 10 octobre à 14h
    const date = new Date(2022, 10, 10, 14);
    vi.setSystemTime(date);

    const res = computeUpdateStatusData(service);
    const label = computeUpdateStatusLabel({ ...res });

    // ALORS l'actualisation est obligatoire et il est considéré comme actualisé il y a 9 mois
    expect(res).toStrictEqual({
      dayDiff: 282,
      weekDiff: 40,
      monthDiff: 9,
      yearDiff: 0,
      updateStatus: "REQUIRED",
    });
    expect(label).toStrictEqual("Actualisé il y a 9 mois");
  });

  test("plus de 10 mois et service en brouillon", () => {
    // ÉTANT DONNÉ un service en brouillon et modifié le 1er janvier à 13h
    const service = {
      modificationDate: new Date(2022, 1, 1, 13),
      status: "DRAFT",
    } as unknown as Service;

    // SI je récupère ses données d'actualisation le 10 octobre à 14h
    const date = new Date(2022, 10, 10, 14);
    vi.setSystemTime(date);

    const res = computeUpdateStatusData(service);
    const label = computeUpdateStatusLabel({ ...res });

    // ALORS l'actualisation n'est pas requise
    expect(res).toStrictEqual({
      dayDiff: 282,
      weekDiff: 40,
      monthDiff: 9,
      yearDiff: 0,
      updateStatus: "NOT_NEEDED",
    });
    expect(label).toStrictEqual("Actualisé il y a 9 mois");
  });

  test("plus de 2 ans et service publié", () => {
    // ÉTANT DONNÉ un service publié et modifié le 1er janvier 2022 à 13h
    const service = {
      modificationDate: new Date(2022, 1, 1, 13),
      status: "PUBLISHED",
    } as unknown as Service;

    // SI je récupère ses données d'actualisation le 1 janvier 2024
    const date = new Date(2024, 10, 10, 14);
    vi.setSystemTime(date);

    const res = computeUpdateStatusData(service);
    const label = computeUpdateStatusLabel({ ...res });

    // ALORS l'actualisation est obligatoire et il est considéré comme actualisé il y a plus de 2 ans
    expect(res).toStrictEqual({
      dayDiff: 1013,
      weekDiff: 144,
      monthDiff: 33,
      yearDiff: 2,
      updateStatus: "REQUIRED",
    });
    expect(label).toStrictEqual("Actualisé il y a plus de 2 ans");
  });

  test("plus de 2 ans et service en brouillon", () => {
    // ÉTANT DONNÉ un service en brouillon et modifié le 1er janvier 2022 à 13h
    const service = {
      modificationDate: new Date(2022, 1, 1, 13),
      status: "DRAFT",
    } as unknown as Service;

    // SI je récupère ses données d'actualisation le 1 janvier 2024
    const date = new Date(2024, 10, 10, 14);
    vi.setSystemTime(date);

    const res = computeUpdateStatusData(service);
    const label = computeUpdateStatusLabel({ ...res });

    // ALORS l'actualisation est obligatoire et il est considéré comme actualisé il y a plus de 2 ans
    expect(res).toStrictEqual({
      dayDiff: 1013,
      weekDiff: 144,
      monthDiff: 33,
      yearDiff: 2,
      updateStatus: "NOT_NEEDED",
    });
    expect(label).toStrictEqual("Actualisé il y a plus de 2 ans");
  });
});
