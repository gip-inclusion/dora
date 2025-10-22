<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import SelectField from "$lib/components/forms/fields/select-field.svelte";
  import { getModel, getServicesOptions } from "$lib/requests/services";
  import { getManagedStructures, getStructure } from "$lib/requests/structures";
  import type {
    Choice,
    Model,
    Service,
    ServicesOptions,
    ShortStructure,
  } from "$lib/types";
  import { debounce } from "$lib/utils/misc";
  import { onMount } from "svelte";

  interface Props {
    servicesOptions: ServicesOptions;
    service: Service;
    managedStructureSearchMode?: boolean;
    structures: ShortStructure[];
    structure?: ShortStructure;
    isModel?: boolean;
    model?: Model | null;
  }

  let {
    servicesOptions = $bindable(),
    service = $bindable(),
    managedStructureSearchMode = false,
    structures,
    structure = $bindable(),
    isModel = false,
    model = $bindable(),
  }: Props = $props();

  const propsWithSpecificFields = [
    "accessConditions",
    "publics",
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
        (option) =>
          !option.structure ||
          (structure?.slug && option.structure === structure.slug)
      );

      if (isModel) {
        // sur un modèle l'API retourne les champs les champs spécifiques sous forme de string,
        // on leur attribue l'id numérique
        service[propName].forEach((value, i) => {
          // si le type est une string, c'est un champs spécifique
          if (typeof value === "string") {
            const option = structureServicesOptions.find(
              (opt) => opt.label === value
            );
            service[propName][i] = option.value;
          }
        });
      } else if (service.model && model) {
        model[propName].forEach((value, i) => {
          // si le type est une string, c'est un champs spécifique
          if (typeof value === "string") {
            const option = structureServicesOptions.find(
              (opt) => opt.label === value
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

      // On rafraîchit les servicesOptions avant qu'elles ne soient modifiées par updateServiceOptions()
      servicesOptions = await getServicesOptions(fetch, false);

      updateServiceOptions();
    }
  }

  async function searchFunction(searchText: string): Promise<Choice[]> {
    if (searchText.length < 3) {
      return [];
    }
    return (await getManagedStructures(searchText)).map((struct) => ({
      value: struct.slug,
      label: struct.name,
    }));
  }

  // Il s'agit d'une édition de service existant
  const showStructures = service.structure
    ? false
    : structures.length > 1 || managedStructureSearchMode;

  onMount(() => {
    if (structure && service.structure) {
      updateServiceOptions();
    }
  });
</script>

<FieldSet noTopPadding>
  <SelectField
    id="structure"
    bind:value={service.structure}
    choices={structures.map((struct) => ({
      value: struct.slug,
      label: struct.name,
    }))}
    onChange={handleStructureChange}
    sort
    searchFunction={managedStructureSearchMode
      ? debounce(searchFunction)
      : undefined}
    disabled={!showStructures}
    placeholder="Sélectionnez la structure…"
    description={managedStructureSearchMode
      ? "Tapez au moins 3 lettres pour lancer la recherche."
      : ""}
  />
</FieldSet>
