<script>
  import { structureStore, servicesStore } from "./_store";

  import LatestServices from "./_latest-services.svelte";
  import StructurePres from "./_structure-pres.svelte";
</script>

<svelte:head>
  <title>{$structureStore.name} | DORA</title>
  <meta name="description" content={$structureStore.shortDesc} />
</svelte:head>

<StructurePres structure={$structureStore} />
<LatestServices
  structure={$structureStore}
  services={$servicesStore.slice(0, 3)}
/>
