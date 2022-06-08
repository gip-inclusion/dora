<script>
  import { moreIcon } from "$lib/icons";

  import ButtonMenu from "$lib/components/button-menu.svelte";
  import ModelMenu from "./model-menu.svelte";

  export let model;
</script>

<ButtonMenu icon={moreIcon} small>
  <ModelMenu {model} />
</ButtonMenu>
