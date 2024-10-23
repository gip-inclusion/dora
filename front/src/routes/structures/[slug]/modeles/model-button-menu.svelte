<script lang="ts">
  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import { moreIcon } from "$lib/icons";
  import ModelMenu from "$lib/components/specialized/services/model-menu.svelte";

  export let model;
  export let readOnly;
</script>

<div class="rounded border border-magenta-cta py-s4">
  <ButtonMenu
    icon={moreIcon}
    small
    hideLabel
    label="Actions disponibles sur le modèle"
  >
    <ModelMenu {model} {readOnly} />
  </ButtonMenu>
</div>
