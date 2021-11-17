<script>
  import { structureStore, servicesStore } from "./_store";

  import AllServices from "./_all_services.svelte";
</script>

<svelte:head>
  <title>Les services | {$structureStore.name} | DORA</title>
  <meta name="description" content={$structureStore.shortDesc} />
</svelte:head>

<AllServices services={$servicesStore} />
