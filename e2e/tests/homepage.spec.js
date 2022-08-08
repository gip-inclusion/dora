import { expect, test } from "@playwright/test";

import { mockServiceOptions } from "../mocks/mockServiceOptions.js";
import { HOME_SELECTORS, HOME_URL } from "../pages/home.js";

test.describe("La page d'accueil", () => {
  test.beforeEach(async ({ context, page }) => {
    await context.route("**/services-options/", (route) =>
      route.fulfill({
        body: JSON.stringify(mockServiceOptions),
      })
    );

    await page.goto(HOME_URL);
    await page.waitForSelector(HOME_SELECTORS.SEARCH_FORM);
  });

  test("a le bon titre", async ({ page }) => {
    const title = await page.textContent("h1");
    expect(title?.trim()).toEqual(
      "Donnez de la visibilité à votre offre d’insertion"
    );
  });

  test("a les bons libellés pour le formulaire de recherche", async ({
    page,
  }) => {
    const formLabels = await page.$$(HOME_SELECTORS.FORM_LABELS);
    expect(formLabels.length).toBe(3);
    expect(await formLabels[0].textContent()).toBe("Thématique");
    expect(await formLabels[1].textContent()).toBe("Besoin");
    expect(await formLabels[2].textContent()).toBe("Lieu");
  });
});
