export function filterAndSortServices(
  services: Array<unknown>,
  searchString: string
): Array<unknown> {
  return (
    searchString
      ? services.filter(
          (entity) =>
            entity.name.toLowerCase().includes(searchString) ||
            entity.structureName.toLowerCase().includes(searchString) ||
            entity.structureDept === searchString
        )
      : services
  )
    .filter((entity) => !entity.parent)
    .sort((entity1, entity2) => {
      if (entity1.structureDept !== entity2.structureDept) {
        return entity1.structureDept.localeCompare(
          entity2.structureDept,
          "fr",
          {
            numeric: true,
          }
        );
      }

      if (
        entity1.structureName.toLowerCase() !==
        entity2.structureName.toLowerCase()
      ) {
        return entity1.structureName
          .toLowerCase()
          .localeCompare(entity2.structureName.toLowerCase(), "fr");
      }

      return entity1.name
        .toLowerCase()
        .localeCompare(entity2.name.toLowerCase(), "fr");
    });
}
