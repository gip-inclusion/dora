<script>
  import { browser } from "$app/env";
  import { page } from "$app/stores";

  import { addCircleIcon, userSmileIcon, loginIcon } from "$lib/icons.js";
  import { userInfo } from "$lib/auth";

  import LinkButton from "$lib/components/link-button.svelte";
  import ButtonMenu from "$lib/components/button-menu.svelte";
  import HamburgerMenu from "$lib/components/hamburger.svelte";
  import TopLinks from "./_top-links.svelte";
  import HeaderMenu from "./_header-menu.svelte";
</script>

{#if browser}
  <HamburgerMenu>
    {#if $userInfo}
      <div class="hidden md:block">
        <ButtonMenu label="Mon compte" icon={userSmileIcon}>
          <HeaderMenu />
        </ButtonMenu>
      </div>
      <div class="block md:hidden">
        <HeaderMenu />
      </div>
      <div class="hidden lg:block">
        <LinkButton
          icon={addCircleIcon}
          to={`/services/creer`}
          ariaLabel="Référencer un service"
        />
      </div>
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
      <div class="block md:hidden">
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
