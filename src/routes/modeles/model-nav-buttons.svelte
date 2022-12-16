<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import { createOrModifyModel } from "$lib/requests/services";
  import { logException } from "$lib/utils/logger";
  import { modelSchema } from "$lib/validation/schemas/service";
  import { validate } from "$lib/validation/validation";

  export let model, onError, servicesOptions;

  async function save() {
    // Validate the whole form
    const { validatedData, valid } = validate(model, modelSchema, {
      servicesOptions: servicesOptions,
    });

    if (valid) {
      // Validation OK, let's send it to the API endpoint
      try {
        const result = await createOrModifyModel(validatedData);
        goto(`/modeles/${result.data.slug}`);
      } catch (error) {
        logException(error);

        if (onError) {
          onError();
        }
      }
    }
  }
</script>

<Button on:click={save} name="save" label="Enregistrer" />
