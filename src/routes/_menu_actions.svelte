<script>
  import { page } from "$app/stores";
  import { browser } from "$app/env";

  import {
    addCircleIcon,
    userSmileIcon,
    loginIcon,
    dashboardIcon,
  } from "$lib/icons.js";
  import { userInfo } from "$lib/auth";

  import LinkButton from "$lib/components/link-button.svelte";
  import ButtonMenu from "$lib/components/button-menu.svelte";
</script>

{#if $page.path !== "/auth/connexion" && browser}
  {#if $userInfo}
    <ButtonMenu label="Mon compte" iconOnLeft icon={userSmileIcon}>
      <LinkButton
        label="Mon espace"
        to={`/tableau-de-bord`}
        icon={dashboardIcon}
        iconOnRight
        noBackground />
      <LinkButton
        label="Deconnexion"
        to={`/auth/deconnexion`}
        icon={loginIcon}
        iconOnRight
        noBackground />
    </ButtonMenu>
    <LinkButton icon={addCircleIcon} to={`/services/creer`} />
  {:else}
    <LinkButton
      label="Inscription"
      icon={loginIcon}
      iconOnLeft
      noBackground
      to={`/auth/inscription`} />

    <LinkButton
      label="Connexion"
      icon={userSmileIcon}
      iconOnLeft
      noBackground
      to={`/auth/connexion?next=${encodeURIComponent($page.path)}`} />
    <LinkButton
      label="Référencer un service"
      icon={addCircleIcon}
      to={`/services/creer`}
      iconOnRight />
  {/if}
{/if}
