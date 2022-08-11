<script>
  import { goto } from "$app/navigation";

  import { validate } from "$lib/validation.js";
  import { modelSchema } from "$lib/schemas/service.js";
  import { createOrModifyModel } from "$lib/services";
  import { logException } from "$lib/logger";

  import Button from "$lib/components/button.svelte";

  export let model, onError, servicesOptions;

  async function save() {
    // Validate the whole form
    const { validatedData, valid } = validate(model, modelSchema, {
      extraData: servicesOptions,
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
