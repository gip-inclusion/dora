<script lang="ts">
  import { moreIcon } from "$lib/icons";
  import type {
    Service,
    ShortService,
    SERVICE_UPDATE_STATUS,
    ServicesOptions,
  } from "$lib/types";

  import ButtonMenu from "$lib/components/button-menu.svelte";
  import ServiceMenu from "./service-menu.svelte";

  export let service: Service | ShortService;
  export let servicesOptions: ServicesOptions;
  export let updateStatus: SERVICE_UPDATE_STATUS | undefined;
  export let onRefresh: () => void | undefined;
</script>

<div class="rounded border border-magenta-cta py-s4">
  <ButtonMenu icon={moreIcon} small>
    <ServiceMenu {service} {servicesOptions} {updateStatus} {onRefresh} />
  </ButtonMenu>
</div>
