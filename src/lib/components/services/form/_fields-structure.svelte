<script>
  import { onMount } from "svelte";

  import { formErrors } from "$lib/validation.js";

  import { getModel, getServicesOptions } from "$lib/services";
  import { getStructure } from "$lib/structures";
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import SchemaField from "$lib/components/forms/schema-field.svelte";

  export let servicesOptions, serviceSchema, service, structures, structure;
  export let isModel = false;
  export let model = null;

  const propsWithSpecificFields = [
    "accessConditions",
    "concernedPublic",
    "requirements",
    "credentials",
  ];

  // met à jour les options de service et le modèle en fonction des champs spécifiques
  // cette fonction est comliqué car sur les champs spécifiques,
  // la `value` peut ĕtre soit une id numérique
  // soit une string sur les modèles.
  // on devrait pourvoir simplifier ici si l'API devient plus cohérente
  function updateServiceOptions() {
    propsWithSpecificFields.forEach((propName) => {
      // options de services qui appartiennent à la structure courante
      const structureServicesOptions = servicesOptions[propName].filter(
        (o) =>
          !o.structure || (structure?.slug && o.structure === structure.slug)
      );

      if (isModel) {
        // sur un modèle l'API retourne les champs les champs spécifiques sous forme de string,
        // on leur attribue l'id numérique
        service[propName].forEach((value, i) => {
          // si le type est une string, c'est un champs spécifique
          if (typeof value === "string") {
            const option = structureServicesOptions.find(
              (o) => o.label === value
            );
            service[propName][i] = option.value;
          }
        });
      } else if (service.model && model) {
        model[propName].forEach((value, i) => {
          // si le type est une string, c'est un champs spécifique
          if (typeof value === "string") {
            const option = structureServicesOptions.find(
              (o) => o.label === value
            );

            // si ce champs spécifique existe dans les options de service
            // -> on modifie le modèle avec l'id du champs spécifique
            // sinon (le champs spécifique n'existe pas dans les options de service)
            // -> on l'ajoute dans les options de service

            if (option) {
              model[propName][i] = option.value;
            } else {
              servicesOptions[propName] = [
                ...servicesOptions[propName],
                { value, label: value },
              ];
            }

            // si on est sur une création de service,
            // le service a été copié depuis le modèle
            // on modifie donc les champs spécifique du service
            if (typeof service[propName][i] === "string") {
              service[propName][i] = option ? option.value : value;
            }
          }
        });
      }
    });
  }

  async function handleStructureChange(slug) {
    if (slug) {
      structure = await getStructure(slug);

      service.structure = slug;
      if (!isModel && service.model) {
        model = await getModel(model.slug);
      }
      servicesOptions = isModel
        ? await getServicesOptions({ model: service })
        : await getServicesOptions({ model });

      updateServiceOptions();
    }
  }

  // Il s'agit d'une édition de service existant
  const showStructures = service.structure ? false : structures.length > 1;

  onMount(() => {
    if (structure && service.structure) {
      updateServiceOptions();
    }
  });
</script>

<FieldSet noTopPadding>
  <SchemaField
    type="select"
    schema={serviceSchema.structure}
    label={serviceSchema.structure.name}
    choices={structures.map((s) => ({ value: s.slug, label: s.name }))}
    name="structure"
    errorMessages={$formErrors.structure}
    bind:value={service.structure}
    onSelectChange={handleStructureChange}
    sortSelect
    placeholder="Sélectionner"
    disabled={!showStructures}
  />
</FieldSet>
