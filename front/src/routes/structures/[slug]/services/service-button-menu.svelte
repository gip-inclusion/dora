<script lang="ts">
  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import { moreIcon } from "$lib/icons";
  import type { Service, ServicesOptions, ShortService } from "$lib/types";
  import ServiceMenu from "./service-menu.svelte";

  interface Props {
    service: Service | ShortService;
    servicesOptions: ServicesOptions;
    onRefresh: () => void;
  }

  let { service, servicesOptions, onRefresh }: Props = $props();
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
