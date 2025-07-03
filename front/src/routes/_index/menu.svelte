<script lang="ts">
  import { run } from 'svelte/legacy';

  import { page } from "$app/stores";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import type { ShortStructure } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";
  import { getCurrentlySelectedStructure } from "$lib/utils/current-structure";
  import MenuMonCompte from "./menu-mon-compte.svelte";
  import HamburgerMenu from "$lib/components/display/hamburger.svelte";
  import SubMenu from "./sub-menu.svelte";
  import MenuMesStructures from "./menu-mes-structures.svelte";
  import { userPreferences } from "$lib/utils/preferences";

  let structures: ShortStructure[] = $state([]);
  let lastVisitedStructure: ShortStructure | undefined = $state(undefined);

  run(() => {
    structures = $userInfo
      ? [...$userInfo.structures, ...$userInfo.pendingStructures]
      : [];
  });

  run(() => {
    lastVisitedStructure = getCurrentlySelectedStructure(
      $userInfo,
      $userPreferences
    );
  });
</script>

<HamburgerMenu>
  <div class="flex flex-col lg:flex-row print:hidden">
    <div class="my-s20 lg:my-s0 text-center lg:text-left">
      <LinkButton
        to="https://aide.dora.inclusion.beta.gouv.fr/fr/"
        noBackground
        otherTab
        extraClass="mr-s8 text-f14!"
        label="Besoin d’aide ?"
      />
    </div>

    {#if !$userInfo}
      {#if $page.url.pathname !== "/auth/connexion"}
        <LinkButton
          label="Se connecter"
          to={`/auth/connexion?next=${encodeURIComponent(
            $page.url.pathname + $page.url.search
          )}`}
        />
      {/if}
    {:else}
      <div class="hidden lg:flex">
        <MenuMesStructures {structures} {lastVisitedStructure} />
        <MenuMonCompte />
      </div>
    {/if}

    <div class="flex flex-col lg:hidden">
      {#if $userInfo}
        <MenuMesStructures {structures} {lastVisitedStructure} mobileDesign />
        <MenuMonCompte mobileDesign />
      {/if}
      <hr class="-mx-s32 mb-s16 mt-s64" />
      <SubMenu mobileDesign />
    </div>
  </div>
</HamburgerMenu>
