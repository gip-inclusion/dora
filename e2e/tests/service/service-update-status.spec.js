import { expect, test } from "@playwright/test";

import { createFakeService } from "../../mocks/mockService.js";
import { createFakeUser } from "../../mocks/mockUser.js";
import {
  SERVICE_SELECTORS,
  mockGetServiceResponse,
  goToServicePage,
} from "../../pages/service.js";
import { mockUserInfoRequest } from "../../pages/common.js";

test.describe("Page service", () => {
  // *** Affichage correct
  test.describe("Affichage correct", () => {
    test("affiche le bon titre", async ({ page, context }) => {
      // ÉTANT DONNÉ un service
      const SERVICE_NAME = "Mon service";
      const SERVICE = createFakeService({ name: SERVICE_NAME });

      // SI je vais sur la page service
      await mockGetServiceResponse(context, SERVICE);
      await goToServicePage(page, SERVICE);

      // ALORS son nom s'affiche correctement
      const title = await page.textContent(SERVICE_SELECTORS.HEADER_TITLE);
      expect(title).toEqual(SERVICE_NAME);
    });

    test("affiche le status disponible", async ({ page, context }) => {
      // ÉTANT DONNÉ un service disponible
      const SERVICE = createFakeService({ isAvailable: true });

      // SI je vais sur la page service
      await mockGetServiceResponse(context, SERVICE);
      await goToServicePage(page, SERVICE);

      // ALORS il est affiché comme disponible
      const availability = await page.textContent(
        SERVICE_SELECTORS.AVAILIBILITY
      );
      expect(availability?.trim()).toEqual("Service disponible");
    });

    test("affiche le status indisponible", async ({ page, context }) => {
      // ÉTANT DONNÉ un service indisponible
      const SERVICE = createFakeService({ isAvailable: false });

      // SI je vais sur la page service
      await mockGetServiceResponse(context, SERVICE);
      await goToServicePage(page, SERVICE);

      // ALORS il est affiché comme indisponible
      const availability = await page.textContent(
        SERVICE_SELECTORS.AVAILIBILITY
      );
      expect(availability?.trim()).toEqual("Service indisponible");
    });
  });

  // *** Actualisation côté offreur
  test.describe("Actualisation côté offreur", () => {
    test("actualisation récente", async ({ page, context }) => {
      // ÉTANT DONNÉ un service actualisé récemment
      // ET en tant qu'utilisateur non connecté
      const today = new Date();

      const SERVICE = createFakeService({
        creationDate: today.toUTCString(),
        modificationDate: today.toUTCString(),
      });

      // SI je vais sur la page service
      await mockGetServiceResponse(context, SERVICE);
      await goToServicePage(page, SERVICE);

      // ALORS le service est affiché comme actualisé récemment
      const updateLabel = await page.textContent(
        SERVICE_SELECTORS.UPDATE_STATUS_LABEL
      );
      expect(updateLabel?.trim()).toEqual("Actualisé aujourd'hui");

      // ET le bouton pour suggérer une modification est visible
      const suggestUpdateButtonText = await page.textContent(
        SERVICE_SELECTORS.UPDATE_STATUS_SUGGEST_BUTTON
      );
      expect(suggestUpdateButtonText?.trim()).toEqual(
        "Suggérer une modification"
      );
    });

    test("aucune actualisation depuis 7 mois", async ({ page, context }) => {
      // ÉTANT DONNÉ un service actualisé il y a 7 mois
      // ET en tant qu'utilisateur non connecté
      const MONTH_DIFF = 7;
      const oldDate = new Date();
      oldDate.setMonth(oldDate.getMonth() - MONTH_DIFF);

      const SERVICE = createFakeService({
        creationDate: oldDate.toUTCString(),
        modificationDate: oldDate.toUTCString(),
      });

      // SI je vais sur la page service
      await mockGetServiceResponse(context, SERVICE);
      await goToServicePage(page, SERVICE);

      // ALORS le service est affiché comme étant actualisé il y a 7 mois
      const updateLabel = await page.textContent(
        SERVICE_SELECTORS.UPDATE_STATUS_LABEL
      );
      expect(updateLabel?.trim()).toContain(
        `Actualisé il y a ${MONTH_DIFF} mois`
      );

      // ET le bouton pour suggérer une modification est visible
      const suggestUpdateButtonText = await page.textContent(
        SERVICE_SELECTORS.UPDATE_STATUS_SUGGEST_BUTTON
      );
      expect(suggestUpdateButtonText?.trim()).toEqual(
        "Suggérer une modification"
      );
    });

    test("aucune actualisation depuis plus depuis 2020", async ({
      page,
      context,
    }) => {
      // ÉTANT DONNÉ un service actualisé il y a longtemps
      // ET en tant qu'utilisateur non connecté
      const oldDate = new Date(2020, 1, 1);

      const SERVICE = createFakeService({
        creationDate: oldDate.toUTCString(),
        modificationDate: oldDate.toUTCString(),
      });

      // SI je vais sur la page service
      await mockGetServiceResponse(context, SERVICE);
      await goToServicePage(page, SERVICE);

      // ALORS le service est affiché comme étant actualisé il y a longtemps
      const updateLabel = await page.textContent(
        SERVICE_SELECTORS.UPDATE_STATUS_LABEL
      );
      expect(updateLabel?.trim()).toContain(
        "Service en attente d’actualisation"
      );

      // ET le bouton pour suggérer une modification est visible
      const suggestUpdateButtonText = await page.textContent(
        SERVICE_SELECTORS.UPDATE_STATUS_SUGGEST_BUTTON
      );
      expect(suggestUpdateButtonText?.trim()).toEqual(
        "Suggérer une modification"
      );
    });
  });

  // *** Actualisation côté administrateur
  test.describe("Actualisation côté administrateur", () => {
    // Création d'un utilisateur gérant une structure
    const STRUCTURE_SLUG = "STRUCTURE_SLUG";
    const STRUCTURE_NAME = "STRUCTURE_NAME";
    const USER = createFakeUser({
      structures: [{ slug: STRUCTURE_SLUG, name: STRUCTURE_NAME }],
    });

    test.beforeEach(async ({ page, context }) => {
      // Faux token pour l'authentification
      await page.addInitScript(() => {
        window.localStorage.setItem("token", "FAKE_TOKEN");
      });

      await mockUserInfoRequest(context, USER);
    });

    test("actualisation récente", async ({ page, context }) => {
      // ÉTANT DONNÉ un service actualisé récemment
      // ET en tant qu'utilisateur gérant la structure
      const today = new Date();

      const SERVICE = createFakeService({
        canWrite: true,
        creationDate: today.toUTCString(),
        modificationDate: today.toUTCString(),
        structureSlug: STRUCTURE_SLUG,
        structureName: STRUCTURE_NAME,
      });

      // SI je vais sur la page service
      await mockGetServiceResponse(context, SERVICE);
      await goToServicePage(page, SERVICE);

      // ALORS le service est affiché comme actualisé récemment
      const updateLabel = await page.textContent(
        SERVICE_SELECTORS.UPDATE_STATUS_LABEL
      );
      expect(updateLabel?.trim()).toEqual("Actualisé aujourd'hui");

      // ET le bouton de mise à jour est visible
      const updateButtonText = await page.textContent(
        SERVICE_SELECTORS.UPDATE_BUTTON
      );
      expect(updateButtonText?.trim()).toEqual("Modifier");

      // ET le bouton de modification du status du service est visible
      const updateServiceStateButtonText = await page.textContent(
        SERVICE_SELECTORS.SERVICE_STATE_UPDATE
      );
      expect(updateServiceStateButtonText?.trim()).toContain(
        "Statut du service"
      );
      expect(updateServiceStateButtonText?.trim()).toContain("Publié");
    });

    test("aucune actualisation depuis 7 mois", async ({ page, context }) => {
      // ÉTANT DONNÉ un service actualisé il y a 7 mois
      // ET en tant qu'utilisateur gérant la structure
      const MONTH_DIFF = 7;
      const oldDate = new Date();
      oldDate.setMonth(oldDate.getMonth() - MONTH_DIFF);

      const SERVICE = createFakeService({
        canWrite: true,
        structureSlug: STRUCTURE_SLUG,
        structureName: STRUCTURE_NAME,
        creationDate: oldDate.toUTCString(),
        modificationDate: oldDate.toUTCString(),
      });

      // SI je vais sur la page service
      await mockGetServiceResponse(context, SERVICE);
      await goToServicePage(page, SERVICE);

      // ALORS le service est affiché comme étant actualisé il y a 7 mois
      const updateLabel = await page.textContent(
        SERVICE_SELECTORS.UPDATE_STATUS_LABEL
      );
      expect(updateLabel?.trim()).toContain("Actualisé il y a 7 mois");
      expect(updateLabel?.trim()).toContain(
        "Vérifiez et/ou actualisez les informations de ce service"
      );

      // ET le bouton de mise à jour est visible
      const updateButtonText = await page.textContent(
        SERVICE_SELECTORS.UPDATE_BUTTON
      );
      expect(updateButtonText?.trim()).toEqual("Modifier");

      // ET le bouton de modification du status du service est visible
      const updateServiceStateButtonText = await page.textContent(
        SERVICE_SELECTORS.SERVICE_STATE_UPDATE
      );
      expect(updateServiceStateButtonText?.trim()).toContain(
        "Statut du service"
      );
      expect(updateServiceStateButtonText?.trim()).toContain("Publié");
    });

    test("aucune actualisation depuis plus depuis 2020", async ({
      page,
      context,
    }) => {
      // ÉTANT DONNÉ un service actualisé il y a longtemps
      // ET en tant qu'utilisateur gérant la structure
      const oldDate = new Date(2020, 1, 1);

      const SERVICE = createFakeService({
        canWrite: true,
        structureSlug: STRUCTURE_SLUG,
        structureName: STRUCTURE_NAME,
        creationDate: oldDate.toUTCString(),
        modificationDate: oldDate.toUTCString(),
      });

      // SI je vais sur la page service
      await mockGetServiceResponse(context, SERVICE);
      await goToServicePage(page, SERVICE);

      // ALORS le service est affiché comme étant actualisé il y a longtemps
      const updateLabel = await page.textContent(
        SERVICE_SELECTORS.UPDATE_STATUS_LABEL
      );
      expect(updateLabel?.trim()).toContain(
        "Service en attente d’actualisation"
      );
      expect(updateLabel?.trim()).toContain(
        "Les informations sur ce service n’ont plus été mises à jour depuis"
      );

      // ET le bouton de mise à jour est visible
      const updateButtonText = await page.textContent(
        SERVICE_SELECTORS.UPDATE_BUTTON
      );
      expect(updateButtonText?.trim()).toEqual("Modifier");

      // ET le bouton de modification du status du service est visible
      const updateServiceStateButtonText = await page.textContent(
        SERVICE_SELECTORS.SERVICE_STATE_UPDATE
      );
      expect(updateServiceStateButtonText?.trim()).toContain(
        "Statut du service"
      );
      expect(updateServiceStateButtonText?.trim()).toContain("Publié");
    });
  });
});
