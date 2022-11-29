export const SERVICE_SELECTORS = {};
SERVICE_SELECTORS.HEADER = "#service-header";
SERVICE_SELECTORS.HEADER_TITLE = `${SERVICE_SELECTORS.HEADER} h1`;
SERVICE_SELECTORS.AVAILIBILITY = `${SERVICE_SELECTORS.HEADER} #service-availability`;
SERVICE_SELECTORS.UPDATE_STATUS = `#service-update-status`;
SERVICE_SELECTORS.UPDATE_STATUS_LABEL = `${SERVICE_SELECTORS.UPDATE_STATUS} #label-container`;
SERVICE_SELECTORS.UPDATE_STATUS_SUGGEST_BUTTON = `${SERVICE_SELECTORS.UPDATE_STATUS} #suggest-update`;
SERVICE_SELECTORS.UPDATE_BUTTON = `${SERVICE_SELECTORS.UPDATE_STATUS} #update`;
SERVICE_SELECTORS.SERVICE_STATE_UPDATE = `${SERVICE_SELECTORS.UPDATE_STATUS} #service-state-update`;

export async function mockGetServiceResponse(context, service) {
  await context.route(`**/services/${service.slug}/`, (route) => {
    return route.fulfill({
      body: JSON.stringify(service),
    });
  });
}

export async function goToServicePage(page, service) {
  await page.goto(`/services/${service.slug}`);
  await page.waitForSelector(SERVICE_SELECTORS.HEADER_TITLE);
}
