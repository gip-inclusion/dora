<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import { GOOGLE_CSE_ID } from "$lib/env";
  import Notice from "$lib/components/display/notice.svelte";
  import { consent } from "$lib/utils/consent.svelte";
</script>

<svelte:head>
  {#if GOOGLE_CSE_ID && consent.consentChoices.googleCSE}
    <!-- Google Custom Search Engine -->
    <script
      async
      src={`https://cse.google.com/cse.js?cx=${GOOGLE_CSE_ID}`}
    ></script>

    <!-- Les couleurs et polices sont définies directement depuis l'interface de gestion du moteur de recherche. -->
    <!-- Pour ce qui est des espacements ou de certains éléments non souhaitables, il faut les gérer ici. -->
    <style>
      .gsc-control-cse {
        padding: 0 !important;
      }
      .gsc-input {
        background: none !important;
      }
      .gcsc-find-more-on-google-branding {
        display: none !important;
      }
    </style>
  {/if}
</svelte:head>

<CenteredGrid>
  <div class="gap-s32 flex flex-col">
    <h1 class="sr-only">
      Résultats de votre recherche de services d’insertion
    </h1>

    <Breadcrumb currentLocation="text-search"></Breadcrumb>

    <div>
      <p class="text-f12 text-gray-text-alt2 italic">
        Saisissez vos mots-clés et cliquez sur la loupe pour lancer la
        recherche.
      </p>
      <div class="gcse-search"></div>
    </div>

    <Notice
      title="Nous expérimentons la recherche par mot-clés pour tester son efficacité"
      type="warning"
      showIcon={false}
    >
      <div>
        Vous allez tester une version expérimentale de notre moteur de
        recherche. Les résultats pourraient être moins précis ou moins nombreux
        qu’une recherche par thématiques ou besoins. Vos retours seront précieux
        pour l’améliorer. <a
          class="text-magenta-cta underline"
          href="https://tally.so/r/mYJ1qW"
          target="_blank">Donnez votre avis</a
        >
      </div>
    </Notice>
  </div>
</CenteredGrid>
