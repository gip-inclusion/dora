import { describe, expect, test } from "vitest";
import { searchDepartment, searchRegion } from "$lib/utils/search-area";

describe("searchDepartment", () => {
  test("basic", () => {
    expect(searchDepartment("Nord")).toEqual({ label: "Nord", code: "59" });
  });
  test("accents", () => {
    expect(searchDepartment("Lozere")).toEqual({ label: "Lozère", code: "48" });
    expect(searchDepartment("Lozère")).toEqual({ label: "Lozère", code: "48" });
  });
  test("case", () => {
    expect(searchDepartment("creuse")).toEqual({ label: "Creuse", code: "23" });
    expect(searchDepartment("CREUSE")).toEqual({ label: "Creuse", code: "23" });
  });
  test("partial", () => {
    expect(searchDepartment("creu")).toEqual({ label: "Creuse", code: "23" });
  });
  describe("Split words", () => {
    test("dash", () => {
      expect(searchDepartment("et loire")).toEqual({
        label: "Indre-et-Loire",
        code: "37",
      });
    });
    test("apostrophe", () => {
      expect(searchDepartment("d'arm")).toEqual({
        label: "Côtes-d'Armor",
        code: "22",
      });
    });
    test("unicode apostrophe", () => {
      expect(searchDepartment("d’arm")).toEqual({
        label: "Côtes-d'Armor",
        code: "22",
      });
    });
    test("space", () => {
      expect(searchDepartment("la re")).toEqual({
        label: "La Réunion",
        code: "974",
      });
    });
  });
  describe("Sorting", () => {
    test("index in searched string", () => {
      // Matches Haute-Vienne and Vienne.
      expect(searchDepartment("vienne")).toEqual({
        label: "Vienne",
        code: "86",
      });
    });
    test("alphabetical", () => {
      // Matches Nord and Normandie.
      expect(searchDepartment("Nor")).toEqual({ label: "Nord", code: "59" });
    });
  });
});

describe("searchRegion", () => {
  test("basic", () => {
    expect(searchRegion("Rhône")).toEqual({
      label: "Auvergne-Rhône-Alpes",
      code: "84",
    });
  });
});
