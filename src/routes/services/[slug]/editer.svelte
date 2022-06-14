<script context="module">
  import { get } from "svelte/store";
  import { browser } from "$app/env";

  import { userInfo } from "$lib/auth";
  import { getServicesOptions, getService, getModel } from "$lib/services";
  import { getStructure, getStructures } from "$lib/structures";

  export async function load({ params }) {
    const user = get(userInfo);
    const service = await getService(params.slug);
    let structure = {};
    let structures = [];
    let model = null;
    const servicesOptions = await getServicesOptions();

    // on ne retourne une 404 que sur le client
    if (!browser) {
      return { structure, structures, service, servicesOptions };
    }

    if (!service) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    structure = await getStructure(service.structure);

    if (user.isStaff) {
      structures = await getStructures();
    } else if (user) {
      structures = user.structures;
    }

    if (service.model) {
      model = await getModel(service.model);
    }

    return {
      props: {
        service,
        servicesOptions,
        structures,
        structure,
        model,
      },
    };
  }
</script>

<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import Fields from "$lib/components/services/form/fields.svelte";
  import ServiceNavButtons from "$lib/components/services/form/service-nav-buttons.svelte";
  import Errors from "$lib/components/services/form/errors.svelte";
  import NoticePublication from "$lib/components/services/form/notice-publication.svelte";

  export let service, servicesOptions, structures, structure, model;

  let errorDiv;

  function onError() {
    errorDiv.scrollIntoView({ behavior: "smooth", block: "start" });
  }
</script>

<svelte:head>
  <title>Éditer | {service?.name} | {structure?.name} | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Modification du service</h1>
    <NoticePublication {service} />
  </CenteredGrid>

  {#if service}
    <div bind:this={errorDiv} />
    <Errors />
    <Fields bind:service {servicesOptions} {structures} {structure} {model} />
    <ServiceNavButtons {onError} bind:service />
  {/if}
</EnsureLoggedIn>
