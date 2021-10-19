<script>
  import { ENVIRONMENT } from "$lib/env.js";

  import NavItem from "$lib/components/nav-item.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import "../../app.postcss";
  import "../../app.css";
  import LogoDORA from "$lib/assets/dora-logo-rvb.svg";
  import LogoMinistere from "$lib/assets/logo-ministere-travail.svg";

  import MenuActions from "./_menu_actions.svelte";
</script>

<style>
  .dev-banner {
    border-top: 8px solid orange;
  }
</style>

<header
  class="grid row-start-1 shadow-md z-10 relative noprint"
  class:dev-banner={ENVIRONMENT !== "production"}>
  <CenteredGrid>
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
        <MenuActions />
      </div>
    </div>
  </CenteredGrid>
  <CenteredGrid gridRow="2" bordertop>
    <nav class="flex flex-row col-span-full">
      <NavItem
        label="Communauté de l’inclusion"
        href="https://communaute.inclusion.beta.gouv.fr/"
        external />
      <NavItem
        label="Contacter l’équipe"
        href="https://itou.typeform.com/doracontactsupp" />
    </nav>
  </CenteredGrid>
</header>
