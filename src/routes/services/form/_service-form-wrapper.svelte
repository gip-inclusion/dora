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

  import NavLink from "./_navlink.svelte";
  import NavButtons from "./_nav-buttons.svelte";

  import serviceSchema, {
    draftServiceSchema,
    step1Schema,
    step2Schema,
    step3Schema,
    step4Schema,
  } from "$lib/schemas/service.js";

  import {
    createOrModifyService,
    getServicesOptions,
    publishDraft,
  } from "$lib/services";
  import { assert, logException } from "$lib/logger";
  import Preview from "./_preview.svelte";
  import Alert from "$lib/components/forms/alert.svelte";

  const schemas = new Map([
    [1, step1Schema],
    [2, step2Schema],
    [3, step3Schema],
    [4, step4Schema],
  ]);

  export let servicesOptions;
  export let title;
  export let currentStep;
  export let service;

  let flashSaveDraftButton = false;

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
        next: 5,
        showPublish: true,
        showPreview: true,
      };
      break;
    case 5:
      navInfo = {
        previous: 4,
        showPublish: true,
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
    // Validate the whole form
    const { _validatedData, valid } = validate(
      service,
      serviceSchema,
      serviceSchema,
      { skipDependenciesCheck: true, noScroll: false }
    );

    if (valid) {
      assert(service.slug);

      // Validation OK, let's send it to the API endpoint
      try {
        const result = await publishDraft(service.slug);
        goto(`/services/${result.slug}`);
      } catch (error) {
        logException(error);
      }
    }
  }

  export async function modify() {
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

      const result = await createOrModifyService(validatedData);
      if (result.ok) {
        service = result.data;
        goto(`/services/${service.slug}`);
      } else {
        injectAPIErrors(result.error, {});
      }
    }
  }

  export async function saveDraft() {
    if (!service.isDraft) return;

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
    if (valid) {
      // Validation OK, let's send it to the API endpoint
      const result = await createOrModifyService(validatedData);
      if (result.ok) {
        // We might have added options to the editable multiselect
        servicesOptions = await getServicesOptions();
        service = result.data;
        flashSaveDraftButton = true;
        setTimeout(() => {
          flashSaveDraftButton = false;
        }, 1000);
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
  }

  function goToPage(number) {
    currentStep = number;
    scrollY = 0;
  }

  function handleGoBack() {
    saveDraft();
    goToPage(navInfo.previous);
  }

  async function handleGoForward() {
    await saveDraft();
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
    if (currentStep === 5) {
      publish();
    } else {
      if (
        validate(service, schemas.get(currentStep), serviceSchema, {
          skipDependenciesCheck: true,
          noScroll: false,
        }).valid
      ) {
        await saveDraft();
        publish();
      }
    }
  }

  async function handleModify() {
    if (currentStep === 5) {
      modify();
    } else {
      if (
        validate(service, schemas.get(currentStep), serviceSchema, {
          skipDependenciesCheck: true,
          noScroll: false,
        }).valid
      ) {
        await modify();
      }
    }
  }

  function handleSaveDraft() {
    saveDraft();
  }

  function handlePreview() {
    handleGoForward();
  }

  function handleNavLinkClick(step) {
    goToPage(step);
  }
</script>

<style>
  nav {
    display: flex;
    justify-content: center;
    margin-top: var(--s24);
  }
</style>

<svelte:window bind:scrollY />

{#if currentStep === 5}
  <Preview {service} />
{:else}
  <CenteredGrid topPadded>
    <div class="col-start-1 col-span-full text-center mb-s48">
      <div class="mx-auto">
        <h1 class="text-france-blue text-f45">
          {title}
        </h1>
        <div class="paragraph-small mt-s16">
          Rendez visible votre offre de services sur la plateforme DORA.<br />
          Les champs marqués d’un astérisque<span
            style="color: var(--col-error);">*</span
          > sont obligatoires.
        </div>

        <nav>
          {#each ["Présentation du service", "Conditions d’accès", "Modalités d’accès", "Informations pratiques"] as name, i}
            <NavLink
              lit={currentStep >= i + 1}
              active={currentStep === i + 1}
              {name}
              on:click={() => handleNavLinkClick(i + 1)}
            />
          {/each}
        </nav>
      </div>
    </div>
  </CenteredGrid>
  <CenteredGrid roundedbg>
    <div class="col-span-8 col-start-1 mb-s64">
      <div bind:this={errorDiv}>
        {#each $formErrors.nonFieldErrors || [] as msg}
          <Alert iconOnLeft label={msg} />
        {/each}
      </div>
      <slot />
    </div>
  </CenteredGrid>
{/if}
<CenteredGrid sticky>
  <NavButtons
    _currentPageIsValid={isValid(schemas.get(currentStep))}
    isDraft={service.isDraft}
    onGoBack={handleGoBack}
    onGoForward={handleGoForward}
    onPublish={handlePublish}
    onModify={handleModify}
    onSaveDraft={handleSaveDraft}
    onPreview={handlePreview}
    withBack={!!navInfo?.previous}
    withForward={!!navInfo?.next && !navInfo?.showPreview}
    withPublish={navInfo?.showPublish}
    withPreview={navInfo?.showPreview}
    withDraft={currentStep !== 5 && service.isDraft}
    {flashSaveDraftButton}
  />
</CenteredGrid>
