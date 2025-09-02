<script lang="ts">
  import More2FillSystem from "svelte-remix/More2FillSystem.svelte";

  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import ModelMenu from "$lib/components/specialized/services/model-menu.svelte";

  let { model, readOnly } = $props();
</script>

<div class="border-magenta-cta py-s4 rounded-sm border">
  <ButtonMenu
    icon={More2FillSystem}
    small
    hideLabel
    label="Actions disponibles sur le modèle"
  >
    <ModelMenu {model} {readOnly} />
  </ButtonMenu>
</div>
