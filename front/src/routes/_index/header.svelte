<script lang="ts">
  import { browser } from "$app/environment";
  import { ENVIRONMENT, WARNING_BANNER } from "$lib/env";
  import LogoDORA from "$lib/assets/logos/logo-dora.svg";
  import LogoRepublique from "$lib/assets/logos/logo-rf.svg";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";

  import HeaderActions from "./menu.svelte";
  import SubMenu from "./sub-menu.svelte";
</script>

<header class:dev-banner={ENVIRONMENT !== "production"}>
  <CenteredGrid noPadding extraClass="border-b border-gray-01">
    <div class="flex justify-between lg:items-center">
      <div class="py-s16 flex flex-row items-center">
        <div>
          <img
            class="mr-s40 inline-block"
            src={LogoRepublique}
            alt="République française - Liberté, Égalité, Fraternité"
            width="73"
            height="65"
          />
        </div>
        <a href="/" class="flex items-center">
          <img
            class="mr-s16 inline-block"
            src={LogoDORA}
            alt="Dora - Découvrir, Orienter, Renseigner, Accompagner"
            width="60"
            height="55"
          />
          <div class="hidden md:block">
            <div class="text-f20 text-gray-dark font-bold">DORA</div>
            <div class="text-f14 text-gray-text">Plateforme de l’inclusion</div>
          </div>
        </a>
      </div>

      <div class="align-top print:hidden">
        {#if browser}
          <HeaderActions />
        {/if}
      </div>
    </div>
  </CenteredGrid>

  <CenteredGrid noPadding extraClass="border-b border-gray-01 print:hidden">
    <SubMenu />
  </CenteredGrid>

  {#if WARNING_BANNER}
    <div class="bg-service-orange p-s8 text-center font-bold">
      {WARNING_BANNER}
    </div>
  {/if}
</header>

<style lang="postcss">
  @reference "../../app.css";

  .dev-banner {
    border-top: 8px solid orange;
  }
</style>
