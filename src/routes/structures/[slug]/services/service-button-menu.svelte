<script lang="ts">
  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import { moreIcon } from "$lib/icons";
  import type {
    Service,
    ServicesOptions,
    SERVICE_UPDATE_STATUS,
    ShortService,
  } from "$lib/types";
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
