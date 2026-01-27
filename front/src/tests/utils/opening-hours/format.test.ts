import { describe, expect, test } from "vitest";
import { formatOsmHours } from "$lib/utils/opening-hours/format";

describe("formatOsmHours", () => {
  test("devrait formater des horaires simples", () => {
    const result = formatOsmHours("Mo-Fr 09:00-12:00");

    expect(result).not.toBeNull();
    expect(Array.isArray(result)).toBe(true);
    if (result) {
      expect(result.length).toBeGreaterThan(0);
      // Vérifie que chaque élément est un tuple [string, string]
      result.forEach(([day, hours]) => {
        expect(typeof day).toBe("string");
        expect(typeof hours).toBe("string");
      });
    }
  });

  test("devrait retourner null pour un format invalide", () => {
    const result = formatOsmHours("invalid format");

    expect(result).toBeNull();
  });

  test("devrait formater des horaires avec plusieurs créneaux", () => {
    const result = formatOsmHours("Mo-Fr 09:00-12:00,14:00-18:00");

    expect(result).not.toBeNull();
    if (result) {
      expect(result.length).toBeGreaterThan(0);
      // Vérifie que les heures contiennent le formatage français
      const hoursString = result.map(([, hours]) => hours).join(" ");
      expect(hoursString).toMatch(/h\d{2}/); // Format "09h00" au lieu de "09:00"
    }
  });

  test("devrait inclure les jours de semaine même s'ils sont fermés", () => {
    const result = formatOsmHours("Sa-Su 09:00-12:00");

    expect(result).not.toBeNull();
    if (result) {
      // Les jours de semaine devraient être présents avec "Fermé"
      const weekdays = result.filter(([day]) =>
        ["Lun.", "Mar.", "Mer.", "Jeu.", "Ven."].some((dayName) =>
          day.startsWith(dayName)
        )
      );
      expect(weekdays.length).toBeGreaterThan(0);
      // Au moins un jour de semaine devrait être "Fermé"
      const closedDays = weekdays.filter(([, hours]) => hours === "Fermé");
      expect(closedDays.length).toBeGreaterThan(0);
    }
  });

  test("devrait exclure les weekends fermés", () => {
    const result = formatOsmHours("Mo-Fr 09:00-12:00");

    expect(result).not.toBeNull();
    if (result) {
      // Les weekends fermés ne devraient pas apparaître
      const weekends = result.filter(([day]) =>
        ["Sam.", "Dim."].some((dayName) => day.startsWith(dayName))
      );
      // Si les weekends sont fermés, ils ne devraient pas être dans le résultat
      weekends.forEach(([, hours]) => {
        expect(hours).not.toBe("Fermé");
      });
    }
  });

  test("devrait formater correctement les heures en français", () => {
    const result = formatOsmHours("Mo 09:00-12:00");

    expect(result).not.toBeNull();
    if (result) {
      const mondayEntry = result.find(([day]) => day.startsWith("Lun"));
      if (mondayEntry) {
        const [, hours] = mondayEntry;
        // Devrait contenir "h" au lieu de ":"
        expect(hours).toMatch(/h\d{2}/);
        // Devrait contenir " - " au lieu de "-"
        expect(hours).toContain(" - ");
      }
    }
  });

  test("devrait gérer plusieurs créneaux avec le séparateur français", () => {
    const result = formatOsmHours("Mo 09:00-12:00,14:00-18:00");

    expect(result).not.toBeNull();
    if (result) {
      const mondayEntry = result.find(([day]) => day.startsWith("Lun"));
      if (mondayEntry) {
        const [, hours] = mondayEntry;
        // Devrait contenir " / " pour séparer les créneaux
        expect(hours).toContain(" / ");
      }
    }
  });

  test("devrait gérer une chaîne vide", () => {
    const result = formatOsmHours("");

    expect(result).toBeNull();
  });

  test("devrait gérer des horaires 24/7", () => {
    const result = formatOsmHours("24/7");

    expect(result).not.toBeNull();
    if (result) {
      expect(result.length).toBeGreaterThan(0);
    }
  });

  test("devrait gérer des horaires avec jours spécifiques", () => {
    const result = formatOsmHours("Mo,We,Fr 09:00-12:00");

    expect(result).not.toBeNull();
    if (result) {
      // Devrait contenir au moins lundi, mercredi et vendredi
      const days = result.map(([day]) => day);
      expect(days.length).toBeGreaterThanOrEqual(3);
    }
  });

  test("devrait gérer des horaires avec exceptions", () => {
    const result = formatOsmHours("Mo-Fr 09:00-12:00; Sa 10:00-14:00");

    expect(result).not.toBeNull();
    if (result) {
      expect(result.length).toBeGreaterThan(0);
    }
  });

  test("devrait retourner un format cohérent pour tous les jours", () => {
    const result = formatOsmHours("Mo-Su 09:00-12:00");

    expect(result).not.toBeNull();
    if (result) {
      // Tous les éléments devraient être des tuples [string, string]
      result.forEach((entry) => {
        expect(Array.isArray(entry)).toBe(true);
        expect(entry.length).toBe(2);
        expect(typeof entry[0]).toBe("string"); // Jour
        expect(typeof entry[1]).toBe("string"); // Heures
      });
    }
  });

  test("devrait gérer des horaires avec plages horaires étendues", () => {
    const result = formatOsmHours("Mo-Fr 08:00-20:00");

    expect(result).not.toBeNull();
    if (result) {
      const hoursString = result.map(([, hours]) => hours).join(" ");
      // Devrait contenir les heures formatées
      expect(hoursString).toMatch(/08h00/);
      expect(hoursString).toMatch(/20h00/);
    }
  });
});
