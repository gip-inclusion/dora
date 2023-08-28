<script lang="ts">
  import { page } from "$app/stores";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import type { ShortStructure } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";
  import { userPreferences } from "$lib/utils/preferences";
  import MenuMonCompte from "./menu-mon-compte.svelte";
  import HamburgerMenu from "$lib/components/display/hamburger.svelte";
  import SubMenu from "./sub-menu.svelte";
  import MenuMesStructures from "./menu-mes-structures.svelte";

  let structures: ShortStructure[] = [];
  let lastVisitedStructure: ShortStructure | undefined = undefined;

  $: structures = $userInfo
    ? [...$userInfo.structures, ...$userInfo.pendingStructures]
    : [];

  $: lastVisitedStructure = $userPreferences.visitedStructures.length
    ? structures.find(
        ({ slug }) => slug === $userPreferences.visitedStructures[0]
      )
    : structures[0];
</script>

<HamburgerMenu>
  <div class="flex flex-col print:hidden lg:flex-row">
    <div class="my-s20 text-center lg:my-s0 lg:text-left">
      <LinkButton
        to="https://aide.dora.inclusion.beta.gouv.fr/fr/"
        noBackground
        otherTab
        extraClass="mr-s8 !text-f14"
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
      <hr class="-mx-s32 mt-s64 mb-s16" />
      <SubMenu mobileDesign />
    </div>
  </div>
</HamburgerMenu>
