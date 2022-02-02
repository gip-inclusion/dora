<script>
  import { ENVIRONMENT } from "$lib/env.js";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import LogoDORA from "$lib/assets/dora-logo-rvb.svg";
  import LogoMinistere from "$lib/assets/logo-ministere-travail.svg";

  import HeaderActions from "./_header-actions.svelte";
  import TopLinks from "./_top-links.svelte";
</script>

<header
  class="relative shadow-md noprint"
  class:dev-banner={ENVIRONMENT !== "production"}
>
  <CenteredGrid>
    <div class="flex flex-row items-center row-start-1 col-span-full py-s12">
      <a class="flex flex-row gap-s40 items-center" href="/">
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
