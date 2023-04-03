import type { Service } from "$lib/types";
import { computeUpdateStatus } from "$lib/utils/service";
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
    // ÉTANT DONNÉ un service publié et modifié à 13h
    const service = {
      modificationDate: new Date(2022, 1, 1, 13),
      status: "PUBLISHED",
    } as unknown as Service;

    // SI je récupère ses données d'actualisation le même jour à 14h
    const date = new Date(2022, 1, 1, 14);
    vi.setSystemTime(date);
    const updateStatus = computeUpdateStatus(service);
    const label = computeRelativeDateLabel(service.modificationDate);

    // ALORS pas d'actualisation nécessaire et il est considéré comme aujourd'hui
    expect(updateStatus).toStrictEqual("NOT_NEEDED");
    expect(label).toStrictEqual("aujourd'hui");
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

    const updateStatus = computeUpdateStatus(service);
    const label = computeRelativeDateLabel(service.modificationDate);

    // ALORS pas d'actualisation nécessaire et il est considéré comme il y a 5 jours
    expect(updateStatus).toStrictEqual("NOT_NEEDED");
    expect(label).toStrictEqual("il y a 5 jours");
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

    const updateStatus = computeUpdateStatus(service);
    const label = computeRelativeDateLabel(service.modificationDate);

    // ALORS pas d'actualisation nécessaire et il est considéré comme il y a 1 semaine
    expect(updateStatus).toStrictEqual("NOT_NEEDED");
    expect(label).toStrictEqual("il y a 1 semaine");
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

    const updateStatus = computeUpdateStatus(service);
    const label = computeRelativeDateLabel(service.modificationDate);

    // ALORS pas d'actualisation nécessaire et il est considéré comme il y a 5 jours
    expect(updateStatus).toStrictEqual("NOT_NEEDED");
    expect(label).toStrictEqual("il y a 3 semaines");
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

    const updateStatus = computeUpdateStatus(service);
    const label = computeRelativeDateLabel(service.modificationDate);

    // ALORS pas d'actualisation nécessaire et il est considéré comme il y a 5 semaines
    expect(updateStatus).toStrictEqual("NOT_NEEDED");
    expect(label).toStrictEqual("il y a 5 semaines");
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

    const updateStatus = computeUpdateStatus(service);
    const label = computeRelativeDateLabel(service.modificationDate);

    // ALORS pas d'actualisation nécessaire et il est considéré comme il y a 3 mois
    expect(updateStatus).toStrictEqual("NOT_NEEDED");
    expect(label).toStrictEqual("il y a 3 mois");
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

    const updateStatus = computeUpdateStatus(service);
    const label = computeRelativeDateLabel(service.modificationDate);

    // ALORS l'actualisation est demandée et il est considéré comme il y a 10 mois
    expect(updateStatus).toStrictEqual("NEEDED");
    expect(label).toStrictEqual("il y a 6 mois");
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

    const updateStatus = computeUpdateStatus(service);
    const label = computeRelativeDateLabel(service.modificationDate);

    // ALORS l'actualisation n'est demandée
    expect(updateStatus).toStrictEqual("NOT_NEEDED");
    expect(label).toStrictEqual("il y a 6 mois");
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

    const updateStatus = computeUpdateStatus(service);
    const label = computeRelativeDateLabel(service.modificationDate);

    // ALORS l'actualisation est obligatoire et il est considéré comme il y a 9 mois
    expect(updateStatus).toStrictEqual("REQUIRED");
    expect(label).toStrictEqual("il y a 9 mois");
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

    const updateStatus = computeUpdateStatus(service);
    const label = computeRelativeDateLabel(service.modificationDate);

    // ALORS l'actualisation n'est pas requise
    expect(updateStatus).toStrictEqual("NOT_NEEDED");
    expect(label).toStrictEqual("il y a 9 mois");
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

    const updateStatus = computeUpdateStatus(service);
    const label = computeRelativeDateLabel(service.modificationDate);

    // ALORS l'actualisation est obligatoire et il est considéré comme il y a plus de 2 ans
    expect(updateStatus).toStrictEqual("REQUIRED");
    expect(label).toStrictEqual("il y a plus de 2 ans");
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

    const updateStatus = computeUpdateStatus(service);
    const label = computeRelativeDateLabel(service.modificationDate);

    // ALORS l'actualisation est obligatoire et il est considéré comme il y a plus de 2 ans
    expect(updateStatus).toStrictEqual("NOT_NEEDED");
    expect(label).toStrictEqual("il y a plus de 2 ans");
  });
});
