<script>
  import { goto } from "$app/navigation";

  import { validate, injectAPIErrors } from "$lib/validation.js";
  import schema, { fields, fieldsRequired } from "$lib/schemas/service.js";
  import { createOrModifyService, publishDraft } from "$lib/services";
  import { assert, logException } from "$lib/logger";

  import Button from "$lib/components/button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import { formatSchema } from "$lib/schemas/utils";

  export let onError, service;
  const serviceSchema = formatSchema(
    schema,
    fields.service,
    fieldsRequired.service
  );

  const draftSchema = formatSchema(
    schema,
    fields.service,
    fieldsRequired.draft
  );

  async function publish() {
    service.isDraft = false;
    service.markSynced = true;

    // Validate the whole form
    const { validatedData, valid } = validate(service, serviceSchema);

    if (valid) {
      // Validation OK, let's send it to the API endpoint
      try {
        let result = await createOrModifyService(validatedData);
        result = await publishDraft(result.data.slug);
        goto(`/services/${result.slug}`);
      } catch (error) {
        logException(error);
      }
    }
  }

  async function saveDraft() {
    service.isDraft = true;
    service.markSynced = true;

    // eslint-disable-next-line no-warning-comments
    // HACK: Empty <Select> are casted to null for now
    // but the server wants an empty string
    // We should fix the <Select> instead
    if (service.category == null) {
      service.category = "";
    }

    const { validatedData, valid } = validate(service, draftSchema);

    if (!valid) {
      return;
    }

    assert(service.slug);

    // Validation OK, let's send it to the API endpoint
    const result = await createOrModifyService(validatedData);

    if (result.ok) {
      // We might have added options to the editable multiselect

      service = result.data;

      goto(`/services/${service.slug}`);
    } else {
      injectAPIErrors(
        result.error || {
          nonFieldErrors: [
            {
              code: "fetch-error",
              message: "Erreur de connexion au serveur",
            },
          ],
        },
        {}
      );

      if (onError) {
        onError();
      }
    }
  }
</script>

<CenteredGrid>
  <div class="flex flex-row gap-s12">
    <Button
      on:click={saveDraft}
      name="save"
      label="Enregistrer en brouillon"
      secondary
    />

    <Button on:click={publish} name="publish" label="Publier" />
  </div>
</CenteredGrid>
