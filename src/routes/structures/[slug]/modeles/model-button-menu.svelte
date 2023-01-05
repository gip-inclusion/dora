<script lang="ts">
  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import { moreIcon } from "$lib/icons";
  import ModelMenu from "$lib/components/specialized/services/model-menu.svelte";

  export let model;
  export let readOnly;
</script>

<ButtonMenu icon={moreIcon} small>
  <ModelMenu {model} {readOnly} />
</ButtonMenu>
