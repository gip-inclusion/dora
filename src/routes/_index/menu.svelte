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

  $: structures = $userInfo
    ? [...$userInfo.structures, ...$userInfo.pendingStructures].sort((a, b) => {
        // si l'utilisateur a visité la page de la structure
        // elle est remontée en tête de liste
        if (
          $userPreferences.visitedStructures.includes(a.slug) &&
          !$userPreferences.visitedStructures.includes(b.slug)
        ) {
          return -1;
        }

        if (
          !$userPreferences.visitedStructures.includes(a.slug) &&
          $userPreferences.visitedStructures.includes(b.slug)
        ) {
          return 1;
        }

        if (
          $userPreferences.visitedStructures.includes(a.slug) &&
          $userPreferences.visitedStructures.includes(b.slug)
        ) {
          return $userPreferences.visitedStructures.indexOf(a.slug) <
            $userPreferences.visitedStructures.indexOf(b.slug)
            ? -1
            : 1;
        }

        // les structures dont l'utilisateur n'a pas visité la page
        // restent en fin de liste par ordre alphabétique
        return a.name.localeCompare(b.name, "fr", { numeric: true });
      })
    : [];
</script>

<HamburgerMenu>
  <div class="flex flex-col print:hidden lg:flex-row">
    <div class="my-s20 text-center lg:my-s0 lg:text-left">
      <LinkButton
        to="https://aide.dora.inclusion.beta.gouv.fr/fr/"
        noBackground
        otherTab
        extraClass="mr-s8"
        label="Besoin d'aide ?"
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
        <MenuMesStructures {structures} />
        <MenuMonCompte />
      </div>
    {/if}

    <div class="flex flex-col lg:hidden">
      {#if $userInfo}
        <MenuMesStructures {structures} mobileDesign />
        <MenuMonCompte mobileDesign />
      {/if}
      <hr class="-mx-s32 mt-s64 mb-s16" />
      <SubMenu mobileDesign />
    </div>
  </div>
</HamburgerMenu>
