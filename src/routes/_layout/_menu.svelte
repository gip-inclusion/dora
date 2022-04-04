<script>
  import { page } from "$app/stores";

  import { questionFillIcon } from "$lib/icons.js";
  import { userInfo } from "$lib/auth";
  import { shortenString } from "$lib/utils";

  import LinkButton from "$lib/components/link-button.svelte";
  import ButtonMenu from "$lib/components/button-menu.svelte";
  import HamburgerMenu from "$lib/components/hamburger.svelte";
  import MenuMonCompte from "./_menu-mon-compte.svelte";
  import MenuStructures from "./_menu-structures.svelte";
  import MenuAide from "./_menu-aide.svelte";

  let structures = [];

  $: structures = $userInfo
    ? [...$userInfo.structures, ...$userInfo.pendingStructures]
    : [];
</script>

<HamburgerMenu>
  {#if $userInfo}
    <MenuMonCompte />
    {#if !!structures?.length}
      <hr class="my-s8 self-stretch border-t-gray-03" />
      <MenuStructures {structures} />
    {/if}
  {:else if $page.url.pathname !== "/auth/connexion"}
    <LinkButton
      label="Se connecter"
      nofollow
      noBackground
      small
      to={`/auth/connexion?next=${encodeURIComponent($page.url.pathname)}`}
    />
    <hr class="my-s8 self-stretch border-t-gray-03" />
  {/if}
  <MenuAide />
  <div slot="lg" class="flex gap-s40">
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
