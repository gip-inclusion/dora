import { describe, expect, test } from "vitest";
import {
  formatDay,
  getHoursFromStr,
  returnEmptyHoursData,
} from "$lib/utils/opening-hours/parse";
import type { OsmDay } from "$lib/types";

import { INVALID_OPENING_HOURS_MARKER } from "$lib/utils/opening-hours";

describe("returnEmptyHoursData", () => {
  test("devrait retourner une structure complète avec tous les jours", () => {
    const result = returnEmptyHoursData();

    expect(result).toHaveProperty("monday");
    expect(result).toHaveProperty("tuesday");
    expect(result).toHaveProperty("wednesday");
    expect(result).toHaveProperty("thursday");
    expect(result).toHaveProperty("friday");
    expect(result).toHaveProperty("saturday");
    expect(result).toHaveProperty("sunday");
  });

  test("devrait avoir les jours de semaine ouverts par défaut (timeSlot1)", () => {
    const result = returnEmptyHoursData();

    expect(result.monday.timeSlot1.isOpen).toBe(true);
    expect(result.tuesday.timeSlot1.isOpen).toBe(true);
    expect(result.wednesday.timeSlot1.isOpen).toBe(true);
    expect(result.thursday.timeSlot1.isOpen).toBe(true);
    expect(result.friday.timeSlot1.isOpen).toBe(true);
  });

  test("devrait avoir les weekends fermés par défaut", () => {
    const result = returnEmptyHoursData();

    expect(result.saturday.timeSlot1.isOpen).toBe(false);
    expect(result.saturday.timeSlot2.isOpen).toBe(false);
    expect(result.sunday.timeSlot1.isOpen).toBe(false);
    expect(result.sunday.timeSlot2.isOpen).toBe(false);
  });

  test("devrait avoir timeSlot2 fermé pour tous les jours", () => {
    const result = returnEmptyHoursData();

    expect(result.monday.timeSlot2.isOpen).toBe(false);
    expect(result.tuesday.timeSlot2.isOpen).toBe(false);
    expect(result.wednesday.timeSlot2.isOpen).toBe(false);
    expect(result.thursday.timeSlot2.isOpen).toBe(false);
    expect(result.friday.timeSlot2.isOpen).toBe(false);
  });

  test("devrait avoir des chaînes vides pour openAt et closeAt", () => {
    const result = returnEmptyHoursData();

    expect(result.monday.timeSlot1.openAt).toBe("");
    expect(result.monday.timeSlot1.closeAt).toBe("");
    expect(result.monday.timeSlot2.openAt).toBe("");
    expect(result.monday.timeSlot2.closeAt).toBe("");
  });
});

describe("formatDay", () => {
  test("devrait retourner undefined si aucun créneau n'a de valeurs", () => {
    const day: OsmDay = {
      timeSlot1: { isOpen: false, openAt: "", closeAt: "" },
      timeSlot2: { isOpen: false, openAt: "", closeAt: "" },
    };

    expect(formatDay(day, "Mo")).toBeUndefined();
  });

  test("devrait formater un créneau valide", () => {
    const day: OsmDay = {
      timeSlot1: { isOpen: true, openAt: "09:00", closeAt: "12:00" },
      timeSlot2: { isOpen: false, openAt: "", closeAt: "" },
    };

    expect(formatDay(day, "Mo")).toBe("Mo 09:00-12:00");
  });

  test("devrait formater deux créneaux valides", () => {
    const day: OsmDay = {
      timeSlot1: { isOpen: true, openAt: "09:00", closeAt: "12:00" },
      timeSlot2: { isOpen: true, openAt: "14:00", closeAt: "18:00" },
    };

    expect(formatDay(day, "Tu")).toBe("Tu 09:00-12:00,14:00-18:00");
  });

  test("devrait utiliser le marqueur invalide pour un créneau invalide", () => {
    const day: OsmDay = {
      timeSlot1: { isOpen: true, openAt: "12:00", closeAt: "09:00" }, // closeAt < openAt
      timeSlot2: { isOpen: false, openAt: "", closeAt: "" },
    };

    expect(formatDay(day, "We")).toBe(`We ${INVALID_OPENING_HOURS_MARKER}`);
  });

  test("devrait ignorer un créneau fermé même s'il a des valeurs", () => {
    const day: OsmDay = {
      timeSlot1: { isOpen: false, openAt: "09:00", closeAt: "12:00" },
      timeSlot2: { isOpen: false, openAt: "", closeAt: "" },
    };

    // Si le créneau est fermé, il retourne juste le préfixe sans heures
    const result = formatDay(day, "Th");
    expect(result).toBe("Th ");
  });

  test("devrait gérer un créneau avec seulement openAt", () => {
    const day: OsmDay = {
      timeSlot1: { isOpen: true, openAt: "09:00", closeAt: "" },
      timeSlot2: { isOpen: false, openAt: "", closeAt: "" },
    };

    // Un créneau avec seulement openAt est considéré invalide (closeAt vide)
    expect(formatDay(day, "Fr")).toBe(`Fr ${INVALID_OPENING_HOURS_MARKER}`);
  });

  test("devrait gérer un créneau avec seulement closeAt", () => {
    const day: OsmDay = {
      timeSlot1: { isOpen: true, openAt: "", closeAt: "18:00" },
      timeSlot2: { isOpen: false, openAt: "", closeAt: "" },
    };

    // Un créneau avec seulement closeAt est considéré invalide (openAt vide)
    expect(formatDay(day, "Sa")).toBe(`Sa ${INVALID_OPENING_HOURS_MARKER}`);
  });
});

describe("getHoursFromStr", () => {
  test("devrait parser un jour simple", () => {
    const result = getHoursFromStr("Mo 09:00-12:00");

    expect(result.monday.timeSlot1.isOpen).toBe(true);
    expect(result.monday.timeSlot1.openAt).toBe("09:00");
    expect(result.monday.timeSlot1.closeAt).toBe("12:00");
    expect(result.monday.timeSlot2.isOpen).toBe(false);
  });

  test("devrait parser plusieurs jours", () => {
    const result = getHoursFromStr("Mo 09:00-12:00;Tu 14:00-18:00");

    expect(result.monday.timeSlot1.isOpen).toBe(true);
    expect(result.monday.timeSlot1.openAt).toBe("09:00");
    expect(result.monday.timeSlot1.closeAt).toBe("12:00");

    // 14:00 est après-midi, donc va dans timeSlot2
    expect(result.tuesday.timeSlot2.isOpen).toBe(true);
    expect(result.tuesday.timeSlot2.openAt).toBe("14:00");
    expect(result.tuesday.timeSlot2.closeAt).toBe("18:00");
    expect(result.tuesday.timeSlot1.isOpen).toBe(false);
  });

  test("devrait parser un jour avec deux créneaux", () => {
    const result = getHoursFromStr("Mo 09:00-12:00,14:00-18:00");

    expect(result.monday.timeSlot1.isOpen).toBe(true);
    expect(result.monday.timeSlot1.openAt).toBe("09:00");
    expect(result.monday.timeSlot1.closeAt).toBe("12:00");

    expect(result.monday.timeSlot2.isOpen).toBe(true);
    expect(result.monday.timeSlot2.openAt).toBe("14:00");
    expect(result.monday.timeSlot2.closeAt).toBe("18:00");
  });

  test("devrait déterminer le créneau selon l'heure (matin)", () => {
    const result = getHoursFromStr("Mo 09:00-12:00");

    expect(result.monday.timeSlot1.isOpen).toBe(true);
    expect(result.monday.timeSlot1.openAt).toBe("09:00");
    expect(result.monday.timeSlot2.isOpen).toBe(false);
  });

  test("devrait déterminer le créneau selon l'heure (après-midi)", () => {
    const result = getHoursFromStr("Mo 14:00-18:00");

    expect(result.monday.timeSlot2.isOpen).toBe(true);
    expect(result.monday.timeSlot2.openAt).toBe("14:00");
    expect(result.monday.timeSlot2.closeAt).toBe("18:00");
    expect(result.monday.timeSlot1.isOpen).toBe(false);
  });

  test("devrait fermer tous les jours non spécifiés", () => {
    const result = getHoursFromStr("Mo 09:00-12:00");

    expect(result.tuesday.timeSlot1.isOpen).toBe(false);
    expect(result.wednesday.timeSlot1.isOpen).toBe(false);
    expect(result.thursday.timeSlot1.isOpen).toBe(false);
    expect(result.friday.timeSlot1.isOpen).toBe(false);
    expect(result.saturday.timeSlot1.isOpen).toBe(false);
    expect(result.sunday.timeSlot1.isOpen).toBe(false);
  });

  test("devrait parser tous les jours de la semaine", () => {
    const result = getHoursFromStr(
      "Mo 09:00-12:00;Tu 09:00-12:00;We 09:00-12:00;Th 09:00-12:00;Fr 09:00-12:00;Sa 09:00-12:00;Su 09:00-12:00"
    );

    expect(result.monday.timeSlot1.isOpen).toBe(true);
    expect(result.tuesday.timeSlot1.isOpen).toBe(true);
    expect(result.wednesday.timeSlot1.isOpen).toBe(true);
    expect(result.thursday.timeSlot1.isOpen).toBe(true);
    expect(result.friday.timeSlot1.isOpen).toBe(true);
    expect(result.saturday.timeSlot1.isOpen).toBe(true);
    expect(result.sunday.timeSlot1.isOpen).toBe(true);
  });

  test("devrait gérer correctement un format minimal", () => {
    const result = getHoursFromStr("Mo 09:00-12:00");

    // Vérifie que le parsing fonctionne normalement
    expect(result.monday.timeSlot1.isOpen).toBe(true);
    expect(result.monday.timeSlot1.openAt).toBe("09:00");
    expect(result.monday.timeSlot1.closeAt).toBe("12:00");
  });

  test("devrait gérer un créneau vide dans deux créneaux", () => {
    const result = getHoursFromStr("Mo 09:00-12:00,");

    expect(result.monday.timeSlot1.isOpen).toBe(true);
    expect(result.monday.timeSlot1.openAt).toBe("09:00");
    expect(result.monday.timeSlot1.closeAt).toBe("12:00");
    expect(result.monday.timeSlot2.isOpen).toBe(false);
  });
});
