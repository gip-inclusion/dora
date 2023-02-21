<script lang="ts">
  import { page } from "$app/stores";
  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import HamburgerMenu from "$lib/components/display/hamburger.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { questionFillIcon } from "$lib/icons";
  import { userInfo } from "$lib/utils/auth";
  import { shortenString } from "$lib/utils/misc";
  import { userPreferences } from "$lib/utils/preferences";
  import MenuAide from "./menu-aide.svelte";
  import MenuMonCompte from "./menu-mon-compte.svelte";
  import MenuStructures from "./menu-structures.svelte";

  let structures = [];

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
  {#if $userInfo}
    <MenuMonCompte />

    {#if !!structures?.length}
      <hr class="my-s8 self-stretch" />
      <MenuStructures {structures} />
    {/if}
    <hr class="my-s8 self-stretch" />
  {:else if $page.url.pathname !== "/auth/connexion"}
    <LinkButton
      label="Se connecter"
      nofollow
      noBackground
      small
      to={`/auth/connexion?next=${encodeURIComponent(
        $page.url.pathname + $page.url.search
      )}`}
    />
    <hr class="my-s8 self-stretch" />
  {/if}

  <MenuAide />

  <div slot="lg" class="flex items-center gap-s12">
    <ButtonMenu label="Menu d’aide" hideLabel icon={questionFillIcon}>
      <MenuAide />
    </ButtonMenu>
    {#if $userInfo}
      <ButtonMenu label={$userInfo.shortName}>
        <MenuMonCompte />
      </ButtonMenu>

      {#if structures.length === 1}
        <LinkButton
          label={`${shortenString(structures[0].name, 16)}`}
          to={`/structures/${structures[0].slug}`}
          noBackground
        />
      {:else if !!structures?.length}
        <ButtonMenu label="Structures">
          <MenuStructures {structures} />
        </ButtonMenu>
      {/if}
    {:else if $page.url.pathname !== "/auth/connexion"}
      <LinkButton
        label="Se connecter"
        nofollow
        secondary
        to={`/auth/connexion?next=${encodeURIComponent(
          $page.url.pathname + $page.url.search
        )}`}
      />
    {/if}
  </div>
</HamburgerMenu>
