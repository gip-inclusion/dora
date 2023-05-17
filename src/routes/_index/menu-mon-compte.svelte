<script lang="ts">
  import { page } from "$app/stores";
  import DropdownMenu from "$lib/components/display/dropdown-menu.svelte";
  import {
    accountCircleLineIcon,
    logoutBoxLineIcon,
    starSmileLineIcon,
  } from "$lib/icons";

  export let mobileDesign = false;

  const aClass =
    "flex w-full lg:min-w-[200px] items-center p-s12 text-gray-text hover:bg-magenta-10 rounded";
</script>

<DropdownMenu icon={accountCircleLineIcon} label="Mon compte" {mobileDesign}>
  <a href="/mon-compte" class={aClass}>
    <span
      class="mr-s10 inline-block h-s24 w-s24 fill-current"
      class:text-magenta-cta={$page.url.pathname === "/mon-compte"}
      aria-hidden
    >
      {@html accountCircleLineIcon}
    </span>
    Mes informations
  </a>

  <a href="/favoris" class={aClass}>
    <span
      class="mr-s10 inline-block h-s24 w-s24 fill-current"
      class:text-magenta-cta={$page.url.pathname === "/favoris"}
      aria-hidden
    >
      {@html starSmileLineIcon}
    </span>
    Mes favoris
  </a>

  <a href="/auth/deconnexion" class={aClass}>
    <span class="mr-s10 inline-block h-s24 w-s24 fill-current" aria-hidden>
      {@html logoutBoxLineIcon}
    </span>
    Déconnexion
  </a>
</DropdownMenu>
