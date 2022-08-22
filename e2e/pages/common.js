/**
 * Permet de simuler un utilisateur connecté
 */
export async function mockUserInfoRequest(context, user) {
  await context.route(`**/user-info/`, (route) => {
    return route.fulfill({
      body: JSON.stringify(user),
    });
  });
}
