<script context="module">
  import { get } from "svelte/store";

  import { browser } from "$app/env";
  import { userInfo } from "$lib/auth";
  import { getServicesOptions, getService } from "$lib/services";
  import { getStructure, getStructures } from "$lib/structures";

  export async function load({ params }) {
    const user = get(userInfo);
    const service = await getService(params.slug);
    const structure = service ? await getStructure(service.structure) : null;

    let structures = [];

    if (browser && user.isStaff) {
      structures = await getStructures();
    } else if (browser && user) {
      structures = user.structures;
    }

    return {
      props: {
        service,
        servicesOptions: await getServicesOptions(),
        structures,
        structure,
      },
    };
  }
</script>

<script>
  import { validate } from "$lib/validation.js";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import ServiceFormWrapper from "../_form/_service-form-wrapper.svelte";
  import serviceSchema from "$lib/schemas/service.js";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Notice from "$lib/components/notice.svelte";

  export let service, servicesOptions, structures, structure;

  let validation;
  $: validation =
    service &&
    validate(service, serviceSchema, serviceSchema, {
      skipDependenciesCheck: true,
      noScroll: true,
      showErrors: false,
    });

  let errors;
  $: errors = validation?.errorFields.length > 1;
</script>

<svelte:head>
  <title>Éditer | {service?.name} | {service?.structureInfo.name} | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  {#if service}
    <CenteredGrid>
      <div class="col-span-full pt-s48 pb-s24">
        <h1>Modification du service</h1>
        {#if !validation?.valid}
          <Notice
            title={`Information${errors ? "s" : ""} requise${
              errors ? "s" : ""
            } pour publier`}
            type="warning"
          >
            <p class="text-f14 first-letter:capitalize">
              {validation?.errorFields.join(", ")}.
            </p>
          </Notice>
        {/if}
      </div>
    </CenteredGrid>

    <ServiceFormWrapper
      bind:service
      {servicesOptions}
      {structures}
      {structure}
    />
  {/if}
</EnsureLoggedIn>
