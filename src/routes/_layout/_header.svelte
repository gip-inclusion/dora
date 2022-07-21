<script>
  import { ENVIRONMENT } from "$lib/env.js";
  import { browser } from "$app/env";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import LogoDORA from "$lib/assets/dora-logo-rvb.svg";
  import LogoMinistere from "$lib/assets/logo-ministere-travail.svg";

  import HeaderActions from "./_menu.svelte";
</script>

<header
  class="noprint relative shadow-md"
  class:dev-banner={ENVIRONMENT !== "production"}
>
  <CenteredGrid noPadding>
    <div class="flex flex-row items-center py-s12">
      <a class="flex flex-row items-center gap-s40" href="/">
        <div class="hidden lg:block">
          <img
            class="inline"
            src={LogoMinistere}
            alt="Ministère du Travail, du Plein emploi et de l’Insertion"
            width="114"
            height="89"
          />
        </div>
        <img
          class="inline"
          src={LogoDORA}
          alt="Dora - Découvrir, Orienter, Renseigner, Accompagner"
          width="140"
          height="65"
        />
      </a>
      {#if browser}
        <div class="grow" />
        <HeaderActions />
      {/if}
    </div>
  </CenteredGrid>
</header>

<style lang="postcss">
  .dev-banner {
    border-top: 8px solid orange;
  }
</style>
