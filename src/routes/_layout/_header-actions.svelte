<script>
  import { browser } from "$app/env";
  import { page } from "$app/stores";

  import { addCircleIcon, userSmileIcon, loginIcon } from "$lib/icons.js";
  import { userInfo } from "$lib/auth";
  import { shortenString } from "$lib/utils";

  import LinkButton from "$lib/components/link-button.svelte";
  import ButtonMenu from "$lib/components/button-menu.svelte";
  import HamburgerMenu from "$lib/components/hamburger.svelte";
  import TopLinks from "./_top-links.svelte";
  import HeaderMenu from "./_header-menu.svelte";

  let structures = [];
  if ($userInfo) {
    structures = structures.concat(
      $userInfo.structures,
      $userInfo.pendingStructures
    );
  }
</script>

{#if browser}
  <HamburgerMenu>
    {#if $userInfo}
      <div class="block lg:hidden">
        <HeaderMenu {structures} />
      </div>
      <div class="hidden lg:block">
        <ButtonMenu label={$userInfo.shortName} icon={userSmileIcon}>
          <HeaderMenu {structures} />
        </ButtonMenu>
      </div>
      {#if !!structures?.length}
        <div class="hidden lg:block">
          {#if structures.length === 1}
            <LinkButton
              label={`${shortenString(structures[0].name, 16)}`}
              to={`/structures/${structures[0].slug}`}
              noBackground
            />
          {:else}
            <ButtonMenu label="Structures">
              {#each structures as structure}
                <LinkButton
                  label={shortenString(structure.name, 32)}
                  to={`/structures/${structure.slug}`}
                  noBackground
                  small
                />
              {/each}
            </ButtonMenu>
          {/if}
        </div>
      {/if}
    {:else}
      {#if $page.url.pathname !== "/auth/inscription"}
        <LinkButton
          label="Inscription"
          icon={loginIcon}
          noBackground
          to={`/auth/inscription`}
        />
      {/if}
      {#if $page.url.pathname !== "/auth/connexion"}
        <LinkButton
          label="Connexion"
          icon={userSmileIcon}
          noBackground
          nofollow
          to={`/auth/connexion?next=${encodeURIComponent($page.url.pathname)}`}
        />
      {/if}
      <div class="block lg:hidden">
        <div class="border-t border-gray-01" />
        <div class="p-s24 text-right">
          <TopLinks />
        </div>
      </div>
      <div class="hidden lg:block">
        <LinkButton
          label="Référencer un service"
          icon={addCircleIcon}
          to={`/services/creer`}
          iconOnRight
        />
      </div>
    {/if}
  </HamburgerMenu>
{/if}
