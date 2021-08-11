<script>
  import { page } from "$app/stores";
  import { token } from "$lib/auth";
  import LogoRF from "$lib/assets/logo-rf.svg";
  import LogoDORA from "$lib/assets/dora-logo-rvb.svg";
  import LogoMinistere from "$lib/assets/logo-ministere-travail.svg";
  import { addCircleIcon, userSmileIcon } from "$lib/icons.js";
  import LinkButton from "$lib/components/link-button.svelte";
  import NavItem from "$lib/components/nav-item.svelte";

  import "../app.postcss";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
</script>

<header class="grid row-start-1 shadow-md mb-7">
  <CenteredGrid class1="row-start-1">
    <div class="flex flex-row items-center row-start-1 col-span-full py-3/2 ">
      <a class="flex flex-row gap-5 " href="/">
        <img
          class="inline"
          src={LogoMinistere}
          alt=""
          width="114"
          height="89" />
        <img class="inline" src={LogoDORA} alt="Dora" width="140" height="65" />
      </a>
      <div class="flex-grow" />
      <div class="flex flex-row">
        {#if $page.path !== "/login"}
          {#if $token}
            <LinkButton
              label="Deconnexion"
              to={`/logout?next=${encodeURIComponent($page.path)}`}
              icon={userSmileIcon}
              iconOnLeft
              noBackground />
          {:else}
            <LinkButton
              label="Connexion"
              icon={userSmileIcon}
              iconOnLeft
              noBackground
              to={`/login?next=${encodeURIComponent($page.path)}`} />
          {/if}
        {/if}
        <LinkButton
          label="Ajouter une offre"
          icon={addCircleIcon}
          to={`/login?next=${encodeURIComponent($page.path)}`}
          iconOnRight />
      </div>
    </div>
  </CenteredGrid>
  <CenteredGrid class1="row-start-2 border-t border-gray-03">
    <div class="flex flex-row col-span-full ">
      <NavItem label="Forum de l’inclusion" external />
      <NavItem label="Contacter l’équipe" />
    </div>
  </CenteredGrid>
</header>

<div class="grid row-start-2 relative">
  <slot />
</div>

<footer class="grid row-start-3 border-t-2 border-france-blue pt-5/2">
  <CenteredGrid class1="row-start-1 mb-5">
    <div class="col-span-5 col-start-1">
      <a class="block" href="/">
        <img class="inline" src={LogoRF} alt="" width="124" height="110" />
      </a>
    </div>
    <div class="col-span-6 col-start-7 text-sm leading-normal text-gray-text">
      Dora est un service public numérique qui permet aux accompagnateurs des
      personnes en difficulté de trouver rapidement une solution d’insertion
      détaillée sur laquelle ils peuvent orienter leurs bénéficiaires
      rapidement.<br />
      <div class="flex gap-3 mt-2 font-bold">
        <a href="https://gouvernement.fr">gouvernement.fr</a>
        <a href="https://service-public.fr">service-public.fr</a>
        <a href="https://data.gouv.fr">data.gouv.fr</a>
      </div>
    </div>
  </CenteredGrid>
  <CenteredGrid class1="row-start-2 border-t border-gray-03">
    <div class="flex col-start-1 col-span-full">
      <NavItem label="Plan du site" separator light />
      <NavItem label="Accessibilité" separator light />
      <NavItem label="Mentions légales" separator light />
      <NavItem label="Données personnelles" separator light />
      <NavItem label="Gestion des cookies" light />
    </div>
  </CenteredGrid>
</footer>
