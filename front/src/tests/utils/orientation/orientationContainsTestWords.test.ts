import { beforeEach, describe, expect, test } from "vitest";
import type { Orientation } from "$lib/types";
import { TEST_WORDS } from "$lib/consts";
import { orientationContainsTestWords } from "$lib/utils/orientation";

const ORIENTATION_TEMPLATE: Orientation = {
  firstStepDone: false,
  contactBoxOpen: false,
  situation: [],
  situationOther: "",
  requirements: [],
  referentLastName: "",
  referentFirstName: "",
  referentPhone: "",
  referentEmail: "",
  prescriberStructureSlug: "",
  beneficiaryLastName: "",
  beneficiaryFirstName: "",
  beneficiaryAvailability: "",
  beneficiaryContactPreferences: [],
  beneficiaryPhone: "",
  beneficiaryEmail: "",
  beneficiaryOtherContactMethod: "",
  orientationReasons: "",
  attachments: {},
  queryId: "",
  creationDate: "",
  status: "OUVERTE",
  beneficiaryAttachmentsDetails: [],
};

describe("orientationContainsTestWords", () => {
  let orientation = structuredClone(ORIENTATION_TEMPLATE);

  beforeEach(() => {
    orientation = structuredClone(ORIENTATION_TEMPLATE);
  });

  test("détecte les mots de test dans chaque champ vérifié", () => {
    TEST_WORDS.forEach((testWord) => {
      [
        "referentFirstName",
        "referentLastName",
        "referentEmail",
        "beneficiaryFirstName",
        "beneficiaryLastName",
        "beneficiaryEmail",
        "orientationReasons",
      ].forEach((field) => {
        orientation = structuredClone(ORIENTATION_TEMPLATE);
        orientation[field] = testWord;
        expect(orientationContainsTestWords(orientation)).toStrictEqual(
          testWord
        );
      });
    });
  });

  test("détecte les mots de test en début de chaîne", () => {
    TEST_WORDS.forEach((testWord) => {
      orientation.orientationReasons = `${testWord} foo bar`;
      expect(orientationContainsTestWords(orientation)).toStrictEqual(testWord);
    });
  });

  test("détecte les mots de test en milieu de chaîne", () => {
    TEST_WORDS.forEach((testWord) => {
      orientation.orientationReasons = `foo ${testWord} bar`;
      expect(orientationContainsTestWords(orientation)).toStrictEqual(testWord);
    });
  });

  test("détecte les mots de test en fin de chaîne", () => {
    TEST_WORDS.forEach((testWord) => {
      orientation.orientationReasons = `foo bar ${testWord}`;
      expect(orientationContainsTestWords(orientation)).toStrictEqual(testWord);
    });
  });

  test("ne détecte pas les mots de test en début de chaîne comme partie d'un autre mot", () => {
    TEST_WORDS.forEach((testWord) => {
      orientation.orientationReasons = `${testWord}foobar`;
      expect(orientationContainsTestWords(orientation)).toEqual(false);
    });
  });

  test("ne détecte pas les mots de test en milieu de chaîne comme partie d'un autre mot", () => {
    TEST_WORDS.forEach((testWord) => {
      orientation.orientationReasons = `foo${testWord}bar`;
      expect(orientationContainsTestWords(orientation)).toEqual(false);
    });
  });

  test("ne détecte pas les mots de test en fin de chaîne comme partie d'un autre mot", () => {
    TEST_WORDS.forEach((testWord) => {
      orientation.orientationReasons = `foobar${testWord}`;
      expect(orientationContainsTestWords(orientation)).toEqual(false);
    });
  });
});
