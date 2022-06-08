<script>
  import { moreIcon } from "$lib/icons";

  import ButtonMenu from "$lib/components/button-menu.svelte";
  import ServiceMenu from "./service-menu.svelte";

  export let service;
</script>

<ButtonMenu icon={moreIcon} small>
  <ServiceMenu {service} />
</ButtonMenu>
