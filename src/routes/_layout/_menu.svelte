<script>
  import { page } from "$app/stores";

  import { questionFillIcon } from "$lib/icons.js";
  import { userInfo } from "$lib/auth";
  import { userPreferences } from "$lib/preferences";
  import { shortenString } from "$lib/utils";

  import LinkButton from "$lib/components/link-button.svelte";
  import ButtonMenu from "$lib/components/button-menu.svelte";
  import HamburgerMenu from "$lib/components/hamburger.svelte";
  import MenuMonCompte from "./_menu-mon-compte.svelte";
  import MenuStructures from "./_menu-structures.svelte";
  import MenuAide from "./_menu-aide.svelte";

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
      to={`/auth/connexion?next=${encodeURIComponent($page.url.pathname)}`}
    />
    <hr class="my-s8 self-stretch" />
  {/if}

  <MenuAide />

  <div slot="lg" class="flex gap-s12">
    <ButtonMenu icon={questionFillIcon}>
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
        to={`/auth/connexion?next=${encodeURIComponent($page.url.pathname)}`}
      />
    {/if}
  </div>
</HamburgerMenu>
