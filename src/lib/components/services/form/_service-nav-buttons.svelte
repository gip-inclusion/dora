<script>
  import { goto } from "$app/navigation";

  import { validate, injectAPIErrors } from "$lib/validation.js";
  import {
    draftSchema,
    serviceSchema,
    SERVICE_STATUSES,
  } from "$lib/schemas/service.js";
  import { createOrModifyService, publishDraft } from "$lib/services";
  import { logException } from "$lib/logger";

  import Button from "$lib/components/button.svelte";
  import { serviceSubmissionTimeMeter } from "$lib/stores/service-submission-time-meter";

  export let onError, service;

  async function publish() {
    service.status = SERVICE_STATUSES.published;
    service.markSynced = true;

    // Validate the whole form
    const { validatedData, valid } = validate(service, serviceSchema);

    if (valid) {
      try {
        let result = await createOrModifyService({
          ...validatedData,
          durationToAdd: $serviceSubmissionTimeMeter.duration,
        });
        result = await publishDraft(result.data.slug);

        // For feedback modal
        serviceSubmissionTimeMeter.setId(result.slug);

        goto(`/services/${result.slug}`);
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

    // Validation OK, let's send it to the API endpoint
    const result = await createOrModifyService({
      ...validatedData,
      durationToAdd: $serviceSubmissionTimeMeter.duration,
    });

    if (result.ok) {
      serviceSubmissionTimeMeter.clear();

      goto(`/services/${result.data.slug}`);
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
