<script lang="ts">
  import BookmarkLineBusiness from "svelte-remix/BookmarkLineBusiness.svelte";

  import { page } from "$app/stores";
  import DropdownMenu from "$lib/components/display/dropdown-menu.svelte";
  import { OIDC_AUTH_BACKEND } from "$lib/env";
  import {
    accountCircleLineIcon,
    logoutBoxLineIcon,
    notificationIcon,
  } from "$lib/icons";

  export let mobileDesign = false;

  const aClass =
    "flex w-full lg:min-w-[200px] items-center p-s12 text-gray-text hover:bg-magenta-10 rounded-sm";
</script>

<DropdownMenu label="Mon compte" {mobileDesign}>
  <a href="/mon-compte" class={aClass}>
    <span
      class="mr-s10 h-s24 w-s24 inline-block fill-current"
      class:text-magenta-cta={$page.url.pathname === "/mon-compte"}
      aria-hidden="true"
    >
      {@html accountCircleLineIcon}
    </span>
    Mes informations
  </a>

  <a href="/favoris" class={aClass}>
    <span
      class="mr-s10 h-s24 w-s24 inline-block fill-current"
      class:text-magenta-cta={$page.url.pathname === "/favoris"}
      aria-hidden="true"
    >
      <BookmarkLineBusiness />
    </span>
    Mes favoris
  </a>

  <a href="/mes-alertes" class={aClass}>
    <span
      class="mr-s10 h-s24 w-s24 inline-block fill-current"
      class:text-magenta-cta={$page.url.pathname === "/mes-alertes"}
      aria-hidden="true"
    >
      {@html notificationIcon}
    </span>Mes alertes
  </a>

  <hr />

  {#if OIDC_AUTH_BACKEND === "proconnect"}
    <a href="/auth/pc-logout" class={aClass}>
      <span
        class="mr-s10 h-s24 w-s24 inline-block fill-current"
        aria-hidden="true"
      >
        {@html logoutBoxLineIcon}
      </span>
      Déconnexion
    </a>
  {:else}
    <a href="/auth/deconnexion" class={aClass}>
      <span
        class="mr-s10 h-s24 w-s24 inline-block fill-current"
        aria-hidden="true"
      >
        {@html logoutBoxLineIcon}
      </span>
      Déconnexion
    </a>
  {/if}
</DropdownMenu>
