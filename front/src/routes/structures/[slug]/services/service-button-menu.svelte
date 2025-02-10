<script lang="ts">
  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import { moreIcon } from "$lib/icons";
  import type { Service, ServicesOptions, ShortService } from "$lib/types";
  import ServiceMenu from "./service-menu.svelte";

  export let service: Service | ShortService;
  export let servicesOptions: ServicesOptions;
  export let onRefresh: () => void | undefined;
</script>

<div class="border-magenta-cta py-s4 rounded-sm border">
  <ButtonMenu
    icon={moreIcon}
    small
    hideLabel
    label="Actions disponibles sur le service"
  >
    <ServiceMenu {service} {servicesOptions} {onRefresh} />
  </ButtonMenu>
</div>
