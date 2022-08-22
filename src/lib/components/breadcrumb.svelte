<script lang="ts">
  // Source pour l'accessibilité : https://www.w3.org/WAI/ARIA/apg/example-index/breadcrumb/index.html
  import type { Structure, Service } from "$lib/types";

  type BreadcrumbLocation = "home" | "structure" | "service";

  export let structure: Structure;
  export let service: Service;
  export let currentLocation: BreadcrumbLocation;
</script>

<nav aria-label="Fil d'ariane">
  <ol class="text-f14">
    <li class="inline">
      <a
        href={"/"}
        aria-current={currentLocation === "home" ? "page" : null}
        class:current={currentLocation === "home"}
        title="Retour à l'accueil du site">Accueil</a
      >
    </li>
    <li class="inline before:content-['/']">
      <a
        href="/structures/{structure.slug}"
        class:current={currentLocation === "structure"}
        aria-current={currentLocation === "structure" ? "page" : null}
        ><span class="hidden lg:inline">Structure&nbsp;•&nbsp;</span
        >{structure.name}</a
      >
    </li>
    {#if service}
      <li class="inline before:content-['/']">
        <a
          href="/services/{service.slug}"
          class:current={currentLocation === "service"}
          aria-current={currentLocation === "service" ? "page" : null}
          ><span class="hidden lg:inline">Service&nbsp;•&nbsp;</span
          >{service.name}</a
        >
      </li>
    {/if}
  </ol>
</nav>

<style lang="postcss">
  a {
    @apply text-magenta-40 print:text-france-blue;
  }

  .current {
    @apply font-bold text-white print:text-france-blue;
  }

  nav li + li::before {
    @apply ml-s8 mr-s8 inline text-magenta-40 print:text-france-blue;
  }
</style>
