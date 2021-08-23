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
    serviceCache,
    resetServiceCache,
    persistServiceCache,
  } from "./_stores.js";
  import NavButtons from "./_nav-buttons.svelte";

  import serviceSchema, {
    step1,
    step2,
    step3,
    step4,
  } from "$lib/schemas/service.js";

  import Step1 from "./_step1.svelte";
  import Step2 from "./_step2.svelte";
  import Step3 from "./_step3.svelte";
  import Step4 from "./_step4.svelte";
  import { createService, modifyService } from "$lib/services";

  export let title;
  export let currentStep = Step1;
  export let modify = false;

  function handleEltChange(evt) {
    // We want to listen to both DOM and component events
    const fieldname = evt.target?.name || evt.detail;
    // Sometimes (particularly with Select components), the event is received
    // before the field value is updated in  $serviceCache, although it's not
    // supposed to happen. This setTimeout is a unsatisfying workaround to that.
    setTimeout(() => {
      const filteredSchema = Object.fromEntries(
        Object.entries(serviceSchema).filter(
          ([name, _rules]) => name === fieldname
        )
      );
      const { validatedData, valid } = validate(
        $serviceCache,
        filteredSchema,
        serviceSchema,
        { skipDependenciesCheck: false, noScroll: true }
      );
      if (valid) {
        $serviceCache = { ...$serviceCache, ...validatedData };
      }
    }, 100);
  }

  setContext(contextValidationKey, {
    onBlur: handleEltChange,
    onChange: handleEltChange,
  });

  let navInfo = {};
  let scrollY;

  $: switch (currentStep) {
    case Step1:
      navInfo = {
        next: Step2,
        schema: step1,
      };
      break;
    case Step2:
      navInfo = {
        previous: Step1,
        next: Step3,
        schema: step2,
      };
      break;
    case Step3:
      navInfo = {
        previous: Step2,
        next: Step4,
        schema: step3,
      };
      break;
    case Step4:
      navInfo = {
        previous: Step3,
        last: true,
        schema: step4,
      };
      break;
    default:
      console.log("?");
  }

  function isValid(_schema) {
    // TODO
    // return schema.isValidSync($serviceCache);
  }

  export async function publish() {
    const { validatedData, valid } = validate(
      $serviceCache,
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
        resetServiceCache();
        goto(`/services/${result.result.slug}`);
      } else {
        injectAPIErrors(result.error, {});
      }
    }
  }

  function handleGoBack() {
    persistServiceCache();
    currentStep = navInfo.previous;
    scrollY = 0;
  }

  function handleGoForward() {
    persistServiceCache();
    if (
      validate($serviceCache, navInfo.schema, serviceSchema, {
        skipDependenciesCheck: true,
        noScroll: false,
      }).valid
    ) {
      currentStep = navInfo.next;
      scrollY = 0;
    }
  }

  function handlePublish() {
    persistServiceCache();
    if (
      validate($serviceCache, navInfo.schema, serviceSchema, {
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
          <NavLink target="etape1" name="Présentation du service" />
          <NavLink target="etape2" name="Conditions d’accès" />
          <NavLink target="etape3" name="Modalités d’accès" />
          <NavLink target="etape4" name="Informations pratiques" />
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
      _currentPageIsValid={isValid(navInfo.schema)}
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
