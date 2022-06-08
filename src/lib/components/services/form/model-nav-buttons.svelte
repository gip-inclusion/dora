<script>
  import { goto } from "$app/navigation";

  import { validate } from "$lib/validation.js";
  import schema, { fields, fieldsRequired } from "$lib/schemas/service.js";
  import { createOrModifyModel } from "$lib/services";
  import { logException } from "$lib/logger";

  import Button from "$lib/components/button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import { formatSchema } from "$lib/schemas/utils";

  export let model;

  const modelSchema = formatSchema(schema, fields.model, fieldsRequired.model);

  async function save() {
    // Validate the whole form
    const { validatedData, valid } = validate(model, modelSchema);

    if (valid) {
      // Validation OK, let's send it to the API endpoint
      try {
        const result = await createOrModifyModel(validatedData);
        goto(`/modeles/${result.data.slug}`);
      } catch (error) {
        logException(error);
      }
    }
  }
</script>

<CenteredGrid>
  <div class="flex flex-row gap-s12">
    <Button on:click={save} name="save" label="Enregistrer" />
  </div>
</CenteredGrid>
