<script>
  import { menuIcon } from "$lib/icons";
  import ButtonMenu from "./button-menu.svelte";
</script>

<div class="flex lg:hidden">
  <ButtonMenu icon={menuIcon}>
    <slot />
  </ButtonMenu>
</div>

<div class="hidden lg:flex">
  <slot name="lg" />
</div>
