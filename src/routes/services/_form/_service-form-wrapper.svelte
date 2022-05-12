<script>
  import { setContext, onMount, onDestroy } from "svelte";

  import { goto } from "$app/navigation";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import {
    validate,
    injectAPIErrors,
    contextValidationKey,
    formErrors,
  } from "$lib/validation.js";

  import Fields from "./_fields.svelte";

  import NavButtons from "./_nav-buttons.svelte";

  import serviceSchema, { draftServiceSchema } from "$lib/schemas/service.js";

  import {
    createOrModifyService,
    getServicesOptions,
    publishDraft,
  } from "$lib/services";
  import { assert, logException } from "$lib/logger";
  import Alert from "$lib/components/forms/alert.svelte";

  export let servicesOptions;
  export let service;
  export let structures;
  export let structure;

  onMount(() => {
    $formErrors = {};
  });

  onDestroy(() => {
    $formErrors = {};
  });

  async function handleEltChange(evt) {
    // We want to listen to both DOM and component events
    const fieldname = evt.target?.name || evt.detail;
    // Sometimes (particularly with Select components), the event is received
    // before the field value is updated in  `service`, although it's not
    // supposed to happen. This setTimeout is a unsatisfying workaround to that.
    await new Promise((resolve) => {
      setTimeout(() => {
        const filteredSchema = Object.fromEntries(
          Object.entries(serviceSchema).filter(
            ([name, _rules]) => name === fieldname
          )
        );
        const { validatedData, valid } = validate(
          service,
          filteredSchema,
          serviceSchema,
          { skipDependenciesCheck: false, noScroll: true }
        );
        if (valid) {
          service = { ...service, ...validatedData };
        }
        resolve();
      }, 200);
    });
  }

  setContext(contextValidationKey, {
    onBlur: handleEltChange,
    onChange: handleEltChange,
  });

  let errorDiv;
  let isValid = false;

  $: isValid = validate(service, serviceSchema, serviceSchema, {
    skipDependenciesCheck: true,
    noScroll: true,
    showErrors: false,
  }).valid;

  async function publish() {
    // Validate the whole form
    const { validatedData, valid } = validate(
      service,
      serviceSchema,
      serviceSchema,
      { skipDependenciesCheck: true, noScroll: false }
    );

    if (valid) {
      assert(service.slug);

      // Validation OK, let's send it to the API endpoint
      try {
        let result = await createOrModifyService(validatedData);
        result = await publishDraft(service.slug);
        goto(`/services/${result.slug}`);
      } catch (error) {
        logException(error);
      }
    }
  }

  async function saveDraft() {
    service.isDraft = true;

    // eslint-disable-next-line no-warning-comments
    // HACK: Empty <Select> are casted to null for now
    // but the server wants an empty string
    // We should fix the <Select> instead
    if (service.category == null) {
      service.category = "";
    }

    const { validatedData, valid } = validate(
      service,
      draftServiceSchema,
      draftServiceSchema,
      { skipDependenciesCheck: true, noScroll: false }
    );

    if (!valid) {
      return;
    }

    assert(service.slug);

    // Validation OK, let's send it to the API endpoint
    const result = await createOrModifyService(validatedData);

    if (result.ok) {
      // We might have added options to the editable multiselect
      servicesOptions = await getServicesOptions();
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

      errorDiv.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  async function handlePublish() {
    if (
      validate(service, serviceSchema, serviceSchema, {
        skipDependenciesCheck: true,
        noScroll: false,
      }).valid
    ) {
      publish();
    }
  }

  function handleSaveDraft() {
    saveDraft();
  }
</script>

<CenteredGrid roundedTop>
  <div class="col-span-full mb-s64 lg:col-span-8 lg:col-start-1">
    <div bind:this={errorDiv}>
      {#each $formErrors.nonFieldErrors || [] as msg}
        <Alert label={msg} />
      {/each}
    </div>
    <Fields bind:service {servicesOptions} {structures} {structure} />
  </div>
</CenteredGrid>

<CenteredGrid>
  <NavButtons
    {isValid}
    onPublish={handlePublish}
    onSaveDraft={handleSaveDraft}
  />
</CenteredGrid>
