<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import SelectField from "$lib/components/inputs/select-field.svelte";
  import { getModel, getServicesOptions } from "$lib/requests/services";
  import { getStructure } from "$lib/requests/structures";
  import type {
    Model,
    Service,
    ServicesOptions,
    ShortStructure,
  } from "$lib/types";
  import type { Schema } from "$lib/validation/schemas/utils";
  import { onMount } from "svelte";

  export let schema: Schema;
  export let servicesOptions: ServicesOptions,
    service: Service,
    structures: ShortStructure[],
    structure: ShortStructure;
  export let isModel = false;
  export let model: Model | undefined = undefined;

  const propsWithSpecificFields = [
    "accessConditions",
    "concernedPublic",
    "requirements",
    "credentials",
  ];

  // met à jour les options de service et le modèle en fonction des champs spécifiques
  // cette fonction est compliquée car sur les champs spécifiques,
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

      servicesOptions = await getServicesOptions();

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
  <SelectField
    id="structure"
    schema={schema.structure}
    bind:value={service.structure}
    choices={structures.map((s) => ({ value: s.slug, label: s.name }))}
    onChange={handleStructureChange}
    sort
    disabled={!showStructures}
    placeholder="Sélectionnez la structure…"
  />
</FieldSet>
