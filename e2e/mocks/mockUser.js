export function createFakeUser({
  email = "example@example.com",
  structures = [],
}) {
  /*
  structures : [
      {
        department: "44",
        modificationDate: "2022-07-01T00:00:00.000000+02:00",
        name: "DAL",
        parent: null,
        slug: "dal",
        typologyDisplay: "Centres provisoires d’hébergement (CPH)",
      },
    ]
    */

  return {
    email,
    firstName: "FirstName",
    fullName: "FirstName LastName",
    isBizdev: false,
    isStaff: false,
    lastName: "LastName",
    newsletter: false,
    pendingStructures: [],
    phoneNumber: "",
    shortName: "Name",
    structures,
  };
}
