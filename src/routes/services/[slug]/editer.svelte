<script context="module">
  import { get } from "svelte/store";
  import { browser } from "$app/env";

  import { userInfo } from "$lib/auth";
  import { getServicesOptions, getService, getModel } from "$lib/services";
  import { getStructure, getStructures } from "$lib/structures";

  export async function load({ params, fetch }) {
    const user = get(userInfo);
    const service = await getService(params.slug, { kitFetch: fetch });
    let structure = {};
    let structures = [];
    let model = null;

    // on ne retourne une 404 que sur le client
    if (!browser) {
      return { structure, structures, service, servicesOptions: {} };
    }

    if (!service) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    structure = await getStructure(service.structure, { kitFetch: fetch });

    if (user.isStaff) {
      structures = await getStructures({ kitFetch: fetch });
    } else if (user) {
      structures = user.structures;
    }

    if (service.model) {
      model = await getModel(service.model, { kitFetch: fetch });
    }

    return {
      props: {
        service,
        servicesOptions: await getServicesOptions({ model, kitFetch: fetch }),
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
  import NoticePublication from "$lib/components/services/form/notice-publication.svelte";
  import ServiceFields from "$lib/components/services/form/service-fields.svelte";

  export let service, servicesOptions, structures, structure, model;
</script>

<svelte:head>
  <title>Éditer | {service?.name} | {structure?.name} | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Modification du service</h1>
    <NoticePublication {service} {servicesOptions} />
  </CenteredGrid>

  <ServiceFields {service} {servicesOptions} {structures} {structure} {model} />
</EnsureLoggedIn>
