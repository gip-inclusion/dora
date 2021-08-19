<script>
  import { setContext } from "svelte";
  import { get } from "svelte/store";

  import { goto } from "$app/navigation";

  import { token } from "$lib/auth";
  import { getApiURL } from "$lib/utils";
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

  export let currentStep = Step1;
  export let modify = false;
  function handleBlur(elt) {
    const schema = serviceSchema.pick([elt.target.name]);
    const validatedData = validate($serviceCache, schema);
    if (validatedData) {
      $serviceCache = { ...$serviceCache, ...validatedData };
    }
  }

  setContext(contextValidationKey, {
    onBlur: handleBlur,
  });

  let navInfo = {};

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

  async function submit(service) {
    const url = modify
      ? `${getApiURL()}/services/${service.slug}/`
      : `${getApiURL()}/services/`;
    const method = modify ? "PATCH" : "POST";

    const res = await fetch(url, {
      method,
      headers: {
        Accept: "application/json; version=1.0",
        "Content-Type": "application/json",

        Authorization: `Token ${get(token)}`,
      },
      body: JSON.stringify(service),
    });

    const result = {
      ok: res.ok,
      status: res.status,
    };
    if (res.ok) {
      result.result = await res.json();
    } else {
      try {
        result.error = await res.json();
      } catch (err) {
        console.error(err);
      }
    }
    return result;
  }

  export async function publish() {
    const validatedData = validate($serviceCache, serviceSchema);

    if (validatedData) {
      // Validation OK, let's send it to the API endpoint
      const result = await submit(validatedData);
      if (result.ok) {
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
  }
  function handleGoForward() {
    persistServiceCache();
    if (validate($serviceCache, navInfo.schema)) {
      console.log("page is valid");
      currentStep = navInfo.next;
    }
  }
  function handlePublish() {
    persistServiceCache();
    if (validate($serviceCache, navInfo.schema)) {
      console.log("page is valid");
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

<EnsureLoggedIn>
  <CenteredGrid>
    <div class="col-start-1 col-span-full text-center mb-6">
      <div class="mx-auto">
        <h1 class="text-france-blue text-13xl">Ajouter un service</h1>
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
