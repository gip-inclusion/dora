<script>
  import { servicesStore } from "./_store";

  import AllServices from "./_all_services.svelte";
</script>

<AllServices services={$servicesStore} />
