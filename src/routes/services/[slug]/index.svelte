<script context="module">
  import { browser } from "$app/env";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import { getService } from "$lib/services";

  export async function load({ params }) {
    const service = await getService(params.slug);
    // si le service est en brouillon il faut un token pour y accéder
    // on renvoit donc un objet vide cŏté serveur
    if (!service && !browser) {
      return {
        props: {
          service: null,
        },
      };
    }

    if (!service) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    return {
      props: {
        service,
      },
    };
  }
</script>

<script>
  import { onMount } from "svelte";
  import ServiceHeader from "$lib/components/services/service-header.svelte";
  import ServiceToolbar from "$lib/components/services/service-toolbar.svelte";
  import ServiceBody from "$lib/components/services/service-body.svelte";

  export let service;

  onMount(() => {
    if (browser) {
      plausible("service", {
        props: {
          service: service.name,
          slug: service.slug,
          structure: service.structureInfo.name,
          departement: service.department,
        },
      });
    }
  });

  async function handleRefresh() {
    service = await getService(service.slug);
  }
</script>

<svelte:head>
  <title>{service?.name} | {service?.structureInfo?.name} | DORA</title>
  <meta name="description" content={service?.shortDesc} />
</svelte:head>

{#if service}
  <CenteredGrid bgColor="bg-gray-bg">
    <ServiceHeader {service} />
  </CenteredGrid>
  <hr />
  <CenteredGrid noPadding>
    <div class="noprint py-s24">
      {#if browser}
        <ServiceToolbar {service} onRefresh={handleRefresh} />
      {/if}
    </div>
  </CenteredGrid>

  <CenteredGrid>
    <ServiceBody {service} />
  </CenteredGrid>
{/if}
