<script lang="ts">
  import type { Service, ShortService } from "$lib/types";
  import ServiceContact from "./display/service-contact.svelte";

  export let service: Service | ShortService;
  export let useWhiteText = true;
</script>

<ServiceContact {service} {useWhiteText} />
