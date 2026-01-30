<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import FormErrors from "$lib/components/forms/form-errors.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import { createStructure, modifyStructure } from "$lib/requests/structures";
  import type { Structure, StructuresOptions } from "$lib/types";
  import { structureSchema } from "$lib/validation/schemas/structure";
  import StructureEditionFields from "./structure-edition-fields.svelte";

  interface Props {
    structure: Structure;
    structuresOptions: StructuresOptions;
    modify?: boolean;
    onRefresh?: () => Promise<void>;
  }

  let {
    structure = $bindable(),
    structuresOptions,
    modify = false,
    onRefresh,
  }: Props = $props();

  let requesting = $state(false);

  const serverErrors = {
    _default: {},
    siret: { unique: "Cette structure existe déjà" },
  };

  function handleChange(validatedData) {
    structure = { ...structure, ...validatedData };
  }

  function handleSubmit(validatedData) {
    return modify
      ? modifyStructure(validatedData)
      : createStructure(validatedData);
  }

  async function handleSuccess(result) {
    if (modify && onRefresh) {
      await onRefresh();
    }
    goto(`/structures/${result.slug}`);
  }
</script>

<FormErrors />

<div class="lg:w-2/3">
  <Form
    bind:data={structure}
    serverErrorsDict={serverErrors}
    schema={structureSchema}
    onChange={handleChange}
    onSubmit={handleSubmit}
    onSuccess={handleSuccess}
    bind:requesting
  >
    <Fieldset>
      <StructureEditionFields bind:structure {structuresOptions} />
    </Fieldset>

    <div class="mt-s32 gap-s16 flex flex-col justify-end md:flex-row">
      <LinkButton
        to="/structures/{structure.slug}"
        secondary
        label="Annuler les modifications"
      />
      <Button
        name="validate"
        type="submit"
        label="Valider les modifications"
        loading={requesting}
      />
    </div>
  </Form>
</div>
