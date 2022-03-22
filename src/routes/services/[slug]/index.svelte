<script context="module">
  import { browser } from "$app/env";
  import { getService } from "$lib/services";

  export async function load({ params }) {
    const service = await getService(params.slug);

    // sur le serveur, info est toujours null,
    // on ne retourne une 404 que sur le client
    if (!service && !browser) {
      return {};
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
  import ServiceCard from "./_service-card.svelte";

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
</script>

<svelte:head>
  <title>{service?.name} | {service?.structureInfo.name} | DORA</title>
  <meta name="description" content={service?.shortDesc} />
</svelte:head>

{#if service}
  <ServiceCard {service} />
{/if}
