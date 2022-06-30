<script>
  import { setContext, onMount, onDestroy } from "svelte";

  import { goto } from "$app/navigation";

  import {
    validate,
    injectAPIErrors,
    contextValidationKey,
    formErrors,
  } from "$lib/validation.js";
  import { contribSchema } from "$lib/schemas/service.js";
  import { publishServiceSuggestion } from "$lib/services";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import NavButtons from "./_nav-buttons.svelte";
  import Fields from "./_fields.svelte";
  import Alert from "$lib/components/forms/alert.svelte";
  import { id, duration } from "../_store";

  export let servicesOptions, source;

  let service = Object.fromEntries(
    Object.entries(contribSchema).map(([fieldName, props]) => [
      fieldName,
      props.default,
    ])
  );

  async function handleEltChange(evt) {
    // We want to listen to both DOM and component events
    const fieldname = evt.target?.name || evt.detail;
    // Sometimes (particularly with Select components), the event is received
    // before the field value is updated in  `service`, although it's not
    // supposed to happen. This setTimeout is a unsatisfying workaround to that.
    await new Promise((resolve) => {
      setTimeout(() => {
        const filteredSchema =
          fieldname && contribSchema[fieldname]
            ? { [fieldname]: contribSchema[fieldname] }
            : {};

        const { validatedData, valid } = validate(service, filteredSchema, {
          fullSchema: contribSchema,
          noScroll: true,
        });
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
  const requiredFields = Object.keys(contribSchema).filter(
    (k) => contribSchema[k].required
  );

  let currentPageIsValid = false;

  $: currentPageIsValid = requiredFields.every((f) =>
    Array.isArray(service[f]) ? service[f].length : service[f]
  );

  let durationCounter = 0;

  async function handlePublish() {
    // Validate the whole form
    const { valid } = validate(service, contribSchema);

    if (valid) {
      const result = await publishServiceSuggestion(service, source);

      if (result.ok && result.data) {
        $id = result.data.id;
        $duration = durationCounter;
        goto(`/contribuer/merci`);
      } else {
        injectAPIErrors(result.error, {});
      }
    }
  }

  let intervalId;

  onMount(() => {
    $formErrors = {};
    intervalId = setInterval(() => {
      if (document.hasFocus()) {
        durationCounter++;
      }
    }, 1000);
  });

  onDestroy(() => {
    $formErrors = {};
    clearInterval(intervalId);
  });
</script>

<CenteredGrid>
  <div class="text-center">
    <h1 class="text-f45 text-france-blue">Proposez un service</h1>
    <div class="paragraph-small mt-s16">
      Aidez-nous à identifier et référencer l’ensemble de l’offre de
      l’insertion.<br />
      Seuls les champs marqués d’un astérisque<span
        style="color: var(--col-error);">*</span
      > sont obligatoires.
    </div>
  </div>
</CenteredGrid>

<CenteredGrid bgColor="bg-gray-bg">
  <div class="lg:w-2/3">
    <div bind:this={errorDiv}>
      {#each $formErrors.nonFieldErrors || [] as msg}
        <Alert label={msg} />
      {/each}
    </div>
    <Fields bind:service {servicesOptions} />
  </div>
</CenteredGrid>

{#if service.siret}
  <CenteredGrid>
    <NavButtons {currentPageIsValid} onPublish={handlePublish} />
  </CenteredGrid>
{/if}
