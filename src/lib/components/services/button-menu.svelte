<script>
  import { moreIcon } from "$lib/icons";

  import ButtonMenu from "$lib/components/button-menu.svelte";
  import Menu from "./menu.svelte";

  export let service;
</script>

<ButtonMenu icon={moreIcon}>
  <Menu {service} />
</ButtonMenu>
