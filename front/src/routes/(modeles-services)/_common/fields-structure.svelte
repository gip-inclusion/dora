<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import SelectField from "$lib/components/forms/fields/select-field.svelte";
  import { getModel } from "$lib/requests/services";
  import { getManagedStructures, getStructure } from "$lib/requests/structures";
  import type {
    Choice,
    Model,
    Service,
    ServicesOptions,
    ShortStructure,
  } from "$lib/types";
  import { debounce } from "$lib/utils/misc";

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

  async function handleStructureChange(slug) {
    if (slug) {
      structure = await getStructure(slug);

      service.structure = slug;
      if (!isModel && service.model) {
        model = await getModel(model.slug);
      }
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
