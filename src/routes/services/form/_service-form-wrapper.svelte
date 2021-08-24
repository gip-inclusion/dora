<script>
  import { setContext } from "svelte";

  import { goto } from "$app/navigation";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import {
    validate,
    injectAPIErrors,
    contextValidationKey,
  } from "$lib/validation.js";

  import NavLink from "./_navlink.svelte";
  import {
    resetServiceCache,
    persistServiceCache,
    getNewService,
  } from "./_stores.js";
  import NavButtons from "./_nav-buttons.svelte";

  import serviceSchema, {
    step1Schema,
    step2Schema,
    step3Schema,
    step4Schema,
  } from "$lib/schemas/service.js";

  import { createService, modifyService } from "$lib/services";

  const schemas = new Map([
    [1, step1Schema],
    [2, step2Schema],
    [3, step3Schema],
    [4, step4Schema],
  ]);
  export let title;
  export let currentStep = 1;
  export let modify = false;
  export let service;
  export let useLocalStorage = false;

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

  $: switch (currentStep) {
    case 1:
      navInfo = {
        next: 2,
      };
      break;
    case 2:
      navInfo = {
        previous: 1,
        next: 3,
      };
      break;
    case 3:
      navInfo = {
        previous: 2,
        next: 4,
      };
      break;
    case 4:
      navInfo = {
        previous: 3,
        last: true,
      };
      break;
    default:
      console.log("?");
  }

  function isValid(_schema) {
    // TODO
    // return schema.isValidSync(service);
  }

  export async function publish() {
    const { validatedData, valid } = validate(
      service,
      serviceSchema,
      serviceSchema,
      { skipDependenciesCheck: true, noScroll: false }
    );
    if (valid) {
      // Validation OK, let's send it to the API endpoint
      let result;
      if (modify) {
        result = await modifyService(validatedData);
      } else {
        result = await createService(validatedData);
      }
      if (result?.ok) {
        if (useLocalStorage) resetServiceCache();
        service = getNewService();
        goto(`/services/${result.result.slug}`);
      } else {
        injectAPIErrors(result.error, {});
      }
    }
  }

  function goToPage(number) {
    if (useLocalStorage) persistServiceCache(service);
    currentStep = number;
    scrollY = 0;
  }

  function handleGoBack() {
    goToPage(navInfo.previous);
  }

  function handleGoForward() {
    if (
      validate(service, schemas.get(currentStep), serviceSchema, {
        skipDependenciesCheck: true,
        noScroll: false,
      }).valid
    ) {
      goToPage(navInfo.next);
    }
  }

  function handlePublish() {
    if (useLocalStorage) persistServiceCache(service);
    if (
      validate(service, schemas.get(currentStep), serviceSchema, {
        skipDependenciesCheck: true,
        noScroll: false,
      }).valid
    ) {
      publish();
    }
  }
  function handleSaveDraft() {
    console.error("Not implemented");
  }

  function handleNavLinkClick(step) {
    goToPage(step);
  }
</script>

<style>
  h1 + p {
    margin-top: var(--s16);
    color: var(--col-text);
    font-size: var(--f16);
    line-height: var(--s24);
  }

  nav {
    display: flex;
    justify-content: center;
    margin-top: var(--s24);
  }
</style>

<svelte:window bind:scrollY />

<EnsureLoggedIn>
  <CenteredGrid>
    <div class="col-start-1 col-span-full text-center mb-6">
      <div class="mx-auto">
        <h1 class="text-france-blue text-13xl">
          {title}
        </h1>
        <p class="text-gray-text text-base">
          Rendez visible votre offre de services sur la plateforme DORA.<br />
          Les champs marqués d’un astérisque<span
            style="color: var(--col-error);">*</span> sont obligatoires.
        </p>

        <nav>
          {#each ["Présentation du service", "Conditions d’accès", "Modalités d’accès", "Informations pratiques"] as name, i}
            <NavLink
              lit={currentStep >= i + 1}
              active={currentStep === i + 1}
              {name}
              on:click={() => handleNavLinkClick(i + 1)} />
          {/each}
        </nav>
      </div>
    </div>
  </CenteredGrid>
  <CenteredGrid gridRow="2" roundedbg>
    <div class="col-span-8 col-start-1 mb-8">
      <slot />
    </div>
  </CenteredGrid>

  <CenteredGrid gridRow="3" sticky>
    <NavButtons
      _currentPageIsValid={isValid(schemas.get(currentStep))}
      onGoBack={handleGoBack}
      onGoForward={handleGoForward}
      onPublish={handlePublish}
      onSaveDraft={handleSaveDraft}
      withBack={!!navInfo?.previous}
      withForward={!!navInfo?.next}
      withPublish={navInfo?.last}
      withDraft />
  </CenteredGrid>
</EnsureLoggedIn>
