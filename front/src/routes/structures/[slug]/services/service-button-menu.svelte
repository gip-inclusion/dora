<script lang="ts">
  import More2FillSystem from "svelte-remix/More2FillSystem.svelte";

  import ButtonMenu from "$lib/components/display/button-menu.svelte";
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
    icon={More2FillSystem}
    small
    hideLabel
    label="Actions disponibles sur le service"
  >
    <ServiceMenu {service} {servicesOptions} {onRefresh} />
  </ButtonMenu>
</div>
