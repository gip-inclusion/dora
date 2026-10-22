<script lang="ts">
  import FieldSet from "#lib/components/display/fieldset.svelte";
  import SelectField from "#lib/components/forms/fields/select-field.svelte";
  import { getModel } from "#lib/requests/services.js";
  import {
    getManagedStructures,
    getStructure,
  } from "#lib/requests/structures.js";
  import type { Choice, Model, Service, ShortStructure } from "#lib/types.js";
  import { debounce } from "#lib/utils/misc.js";
  import { toServiceStructure } from "#lib/utils/forms.js";

  interface Props {
    service: Service;
    managedStructureSearchMode?: boolean;
    structures: ShortStructure[];
    structure?: ShortStructure;
    isModel?: boolean;
    model?: Model | null;
  }

  let {
    service = $bindable(),
    managedStructureSearchMode = false,
    structures,
    // eslint-disable-next-line @typescript-eslint/no-unused-vars -- prop $bindable() : écrite ici, lue par le parent via le binding (faux positif, cf. @typescript-eslint 8.71.1)
    structure = $bindable(),
    isModel = false,
    model = $bindable(),
  }: Props = $props();

  async function handleStructureChange(slug) {
    if (slug) {
      // variable locale : le prop `structure` est typé `ShortStructure`, trop pauvre
      // pour `toServiceStructure` (ni téléphone, ni courriel, ni horaires).
      const fullStructure = await getStructure(slug);
      structure = fullStructure;

      service.structure = slug;
      if (fullStructure) {
        service.structureInfo = toServiceStructure(fullStructure);
      }
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
