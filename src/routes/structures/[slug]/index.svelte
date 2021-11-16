<script>
  import { structureStore, servicesStore } from "./_store";

  import LatestServices from "./_latest-services.svelte";
  import StructurePres from "./_structure-pres.svelte";
</script>

<StructurePres structure={$structureStore} />
<LatestServices
  structure={$structureStore}
  services={$servicesStore.slice(0, 3)}
/>
