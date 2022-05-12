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

  import NavButtons from "./_nav-buttons.svelte";
  import Fields from "./_fields.svelte";

  import serviceSchema from "$lib/schemas/service-contrib.js";

  import Alert from "$lib/components/forms/alert.svelte";
  import { publishServiceSuggestion } from "$lib/services";

  export let servicesOptions;
  let service = Object.fromEntries(
    Object.entries(serviceSchema).map(([fieldName, props]) => [
      fieldName,
      props.default,
    ])
  );

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
  const requiredFields = Object.keys(serviceSchema).filter(
    (k) => serviceSchema[k].required
  );

  let currentPageIsValid = false;

  $: currentPageIsValid = requiredFields.every((f) =>
    Array.isArray(service[f]) ? service[f].length : service[f]
  );

  async function handlePublish() {
    // Validate the whole form
    if (
      validate(service, serviceSchema, serviceSchema, {
        skipDependenciesCheck: true,
        noScroll: false,
      }).valid
    ) {
      const result = await publishServiceSuggestion(service);
      if (result.ok) {
        goto(`/contribuer/merci`);
      } else {
        injectAPIErrors(result.error, {});
      }
    }
  }
</script>

<CenteredGrid topPadded>
  <div class="col-span-full mb-s48 text-center">
    <div class="mx-auto">
      <h1 class="text-f45 text-france-blue">Proposez un service</h1>
      <div class="paragraph-small mt-s16">
        Aidez-nous à identifier et référencer l’ensemble de l’offre de
        l’insertion.<br />
        Seuls les champs marqués d’un astérisque<span
          style="color: var(--col-error);">*</span
        > sont obligatoires.
      </div>
    </div>
  </div>
</CenteredGrid>
<CenteredGrid roundedTop>
  <div class="col-span-full mb-s64 lg:col-span-8 lg:col-start-1">
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
