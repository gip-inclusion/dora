<script>
  import { ENVIRONMENT } from "$lib/env.js";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import LogoDORA from "$lib/assets/dora-logo-rvb.svg";
  import LogoMinistere from "$lib/assets/logo-ministere-travail.svg";

  import HeaderActions from "./_header-actions.svelte";
  import TopLinks from "./_top-links.svelte";
</script>

<header
  class="noprint relative shadow-md"
  class:dev-banner={ENVIRONMENT !== "production"}
>
  <CenteredGrid>
    <div class="col-span-full row-start-1 flex flex-row items-center py-s12">
      <a class="flex flex-row items-center gap-s40" href="/">
        <div class="hidden lg:block">
          <img
            class="inline"
            src={LogoMinistere}
            alt=""
            width="114"
            height="89"
          />
        </div>
        <img class="inline" src={LogoDORA} alt="Dora" width="140" height="65" />
      </a>
      <div class="grow" />
      <div class="flex flex-row">
        <HeaderActions />
      </div>
    </div>
  </CenteredGrid>
  <div class="hidden md:block">
    <CenteredGrid bordertop>
      <TopLinks />
    </CenteredGrid>
  </div>
</header>

<style lang="postcss">
  .dev-banner {
    border-top: 8px solid orange;
  }
</style>
