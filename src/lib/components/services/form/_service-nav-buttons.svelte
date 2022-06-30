<script>
  import { goto } from "$app/navigation";

  import { validate, injectAPIErrors } from "$lib/validation.js";
  import {
    draftSchema,
    serviceSchema,
    SERVICE_STATUSES,
  } from "$lib/schemas/service.js";
  import { createOrModifyService, publishDraft } from "$lib/services";
  import { assert, logException } from "$lib/logger";

  import Button from "$lib/components/button.svelte";
  import { duration, serviceSlug } from "./_store";

  export let onError, service, durationCounter;

  async function publish() {
    service.status = SERVICE_STATUSES.published;
    service.markSynced = true;

    // Validate the whole form
    const { validatedData, valid } = validate(service, serviceSchema);

    if (valid) {
      try {
        let result = await createOrModifyService(validatedData);
        result = await publishDraft(result.data.slug);
        $serviceSlug = result.slug;
        $duration = durationCounter;
        goto(`/services/${result.slug}/avis`);
      } catch (error) {
        logException(error);
      }
    }
  }

  async function saveDraft() {
    service.status = SERVICE_STATUSES.draft;
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

<Button
  on:click={saveDraft}
  name="save"
  label="Enregistrer en brouillon"
  secondary
/>

<Button on:click={publish} name="publish" label="Publier" />
