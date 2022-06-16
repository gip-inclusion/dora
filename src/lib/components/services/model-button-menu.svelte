<script>
  import { moreIcon } from "$lib/icons";

  import ButtonMenu from "$lib/components/button-menu.svelte";
  import ModelMenu from "./model-menu.svelte";

  export let model;
  export let readOnly;
</script>

<ButtonMenu icon={moreIcon} small>
  <ModelMenu {model} {readOnly} />
</ButtonMenu>
