<script lang="ts">
  import { browser } from "$app/environment";
  import LogoDORA from "$lib/assets/logos/logo-dora.svg";
  import LogoMinistere from "$lib/assets/logos/logo-ministere-travail-emploi.svg";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import { ENVIRONMENT } from "$lib/env";
  import HeaderActions from "./menu.svelte";
</script>

<header
  class="relative shadow-md"
  class:dev-banner={ENVIRONMENT !== "production"}
  role="banner"
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
            height="92"
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
        <div class="print:hidden">
          <HeaderActions />
        </div>
      {/if}
    </div>
  </CenteredGrid>
</header>

<style lang="postcss">
  .dev-banner {
    border-top: 8px solid orange;
  }
</style>
