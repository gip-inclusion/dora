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

  import serviceSchema, {
    step1Schema,
    step2Schema,
  } from "$lib/schemas/service-contrib.js";

  import Alert from "$lib/components/forms/alert.svelte";
  import { publishServiceSuggestion } from "$lib/services";

  const schemas = new Map([
    [1, step1Schema],
    [2, step2Schema],
  ]);

  export let currentStep;
  export let service;

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

  let navInfo = {};
  let scrollY;
  let errorDiv;
  const requiredFields = Object.keys(step1Schema).filter(
    (k) => step1Schema[k].required
  );

  let currentPageIsValid = false;

  $: currentPageIsValid = requiredFields.every((f) =>
    Array.isArray(service[f]) ? service[f].length : service[f]
  );

  $: switch (currentStep) {
    case 1:
      navInfo = {
        next: 2,
      };
      break;
    case 2:
      navInfo = {};
      break;

    default:
      console.warning("?");
  }

  function goToPage(number) {
    currentStep = number;
    scrollY = 0;
  }

  async function handleGoForward() {
    if (
      validate(service, schemas.get(currentStep), serviceSchema, {
        skipDependenciesCheck: true,
        noScroll: false,
      }).valid
    ) {
      goToPage(navInfo.next);
    }
  }

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

<svelte:window bind:scrollY />

<CenteredGrid topPadded>
  <div class="col-span-full col-start-1 mb-s48 text-center">
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
<CenteredGrid roundedbg>
  <div class="col-span-8 col-start-1 mb-s64">
    <div bind:this={errorDiv}>
      {#each $formErrors.nonFieldErrors || [] as msg}
        <Alert label={msg} />
      {/each}
    </div>
    <slot />
  </div>
</CenteredGrid>

{#if service.siret}
  <CenteredGrid sticky>
    <NavButtons
      {currentPageIsValid}
      onGoForward={handleGoForward}
      onPublish={handlePublish}
      withForward={!!navInfo?.next && !navInfo?.showPreview}
    />
  </CenteredGrid>
{/if}
