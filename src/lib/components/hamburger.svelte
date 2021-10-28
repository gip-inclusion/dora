<script>
  import { menuIcon } from "$lib/icons";
  import ButtonMenu from "./button-menu.svelte";
</script>

<div class="flex md:hidden">
  <ButtonMenu icon={menuIcon}>
    <slot />
  </ButtonMenu>
</div>

<div class="hidden md:flex">
  <slot />
</div>
