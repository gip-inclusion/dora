<script>
  import { onMount, setContext } from "svelte";
  import { get } from "svelte/store";

  import { goto } from "$app/navigation";
  import { browser } from "$app/env";

  import { token } from "$lib/auth";
  import { getApiURL } from "$lib/utils";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import {
    validate,
    injectAPIErrors,
    contextValidationKey,
  } from "$lib/validation.js";

  import { serviceOptions } from "./_creation-store.js";
  import NavLink from "./_navlink.svelte";
  import { serviceCache } from "./_creation-store.js";
  import NavButtons from "./_nav-buttons.svelte";
  import { storageKey } from "./_constants.js";

  import serviceSchema, {
    step1,
    step2,
    step3,
    step4,
  } from "$lib/schemas/service.js";
  import { page } from "$app/stores";

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

  const currentPath = $page.path.split("/").pop();
  let navInfo = {
    currentPath,
  };
  switch (currentPath) {
    case "etape1":
      navInfo = {
        next: "etape2",
        schema: step1,
      };
      break;
    case "etape2":
      navInfo = {
        previous: "etape1",
        next: "etape3",
        schema: step2,
      };
      break;
    case "etape3":
      navInfo = {
        previous: "etape2",
        next: "etape4",
        schema: step3,
      };
      break;
    case "etape4":
      navInfo = {
        previous: "etape3",
        last: true,
        schema: step4,
      };
      break;
    default:
      console.log("?");
  }

  onMount(async () => {
    const url = `${getApiURL()}/services/`;
    const res = await fetch(url, {
      method: "OPTIONS",
      headers: {
        Accept: "application/json; version=1.0",
        Authorization: `Token ${$token}`,
      },
    });

    if (res.ok) {
      $serviceOptions = (await res.json()).actions.POST;
    }

    return {
      status: res.status,
      error: new Error(`Could not load ${url}`),
    };
  });

  function clearStore() {
    localStorage.removeItem(storageKey);
  }

  export function persistStore() {
    if (browser) {
      localStorage.setItem(storageKey, JSON.stringify(get(serviceCache)));
    }
  }

  function isValid(schema) {
    return schema.isValidSync($serviceCache);
  }

  async function submit(service) {
    const url = `${getApiURL()}/services/`;
    const res = await fetch(url, {
      method: "POST",
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
        clearStore();
        goto(`../${result.result.id}`);
      } else {
        injectAPIErrors(result.error, {});
      }
    }
  }

  function handleGoBack() {
    persistStore();
    goto(navInfo.previous);
  }
  function handleGoForward() {
    persistStore();
    if (validate($serviceCache, navInfo.schema)) {
      console.log("page is valid");
      goto(navInfo.next);
    }
  }
  function handlePublish() {
    persistStore();
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
