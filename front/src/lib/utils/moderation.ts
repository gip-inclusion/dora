const STATUS_VALUE = {
  NEED_INITIAL_MODERATION: 1,
  NEED_NEW_MODERATION: 2,
  IN_PROGRESS: 3,
  VALIDATED: 4,
};

export function filterAndSortStructures(
  entities: Array<unknown>,
  searchString: string
): Array<unknown> {
  const result = (
    searchString
      ? entities.filter((entity) => {
          if (entity.isStructure) {
            return (
              entity.name.toLowerCase().includes(searchString) ||
              entity.department === searchString
            );
          } else {
            return (
              entity.name.toLowerCase().includes(searchString) ||
              entity.structureName.toLowerCase().includes(searchString) ||
              entity.structureDept === searchString
            );
          }
        })
      : entities
  )
    .filter((entity) => !entity.parent)
    .sort((entity1, entity2) => {
      // On tri d'abord par statut de modération
      const val1 = entity1.moderationStatus
        ? STATUS_VALUE[entity1.moderationStatus]
        : 999;
      const val2 = entity2.moderationStatus
        ? STATUS_VALUE[entity2.moderationStatus]
        : 999;
      if (val1 !== val2) {
        return val1 - val2;
      }
      // Puis les structures en premier
      if (entity1.isStructure && !entity2.isStructure) {
        return -1;
      }
      if (entity2.isStructure && !entity1.isStructure) {
        return 1;
      }
      // Puis par dept de structure
      const sdept1 = entity1.isStructure
        ? entity1.department
        : entity1.structureDept;
      const sdept2 = entity1.isStructure
        ? entity1.department
        : entity1.structureDept;
      if (sdept1 !== sdept2) {
        return sdept1 > sdept2;
      }
      // Puis par nom de structure
      const sname1 = entity1.isStructure ? entity1.name : entity1.structureName;
      const sname2 = entity1.isStructure ? entity1.name : entity1.structureName;
      if (sname1 !== sname2) {
        return sname1 > sname2;
      }
      // Finalement par nom
      return entity1.name > entity2.name;
    });
  return result;
}
