<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";

  import ServiceBeneficiaries from "./service-beneficiaries.svelte";
  import ServiceMobilisation from "./service-mobilisation.svelte";
  import ServiceMobilize from "./service-mobilize.svelte";
  import ServiceShare from "./service-share.svelte";
  import ServicePresentation from "./service-presentation.svelte";
  import ServiceKeyInformations from "$lib/components/specialized/services/service-key-informations.svelte";

  export let service: Service | Model;
  export let servicesOptions: ServicesOptions;
  export let isModel = false;
</script>

<CenteredGrid>
  <div class="service-body">
    <div class="presentation">
      <ServicePresentation {service} {servicesOptions} />
    </div>
    <hr class="separator-1" />
    <div class="beneficiaries">
      <ServiceBeneficiaries {service} />
    </div>
    <hr class="separator-2" />
    <div class="mobilize">
      <ServiceMobilize {service} />
    </div>

    <div class="sidebar flex flex-col gap-y-s24">
      {#if !isModel}
        <div
          class="block rounded-lg border border-gray-02 p-s24 px-s32 print:hidden"
        >
          <ServiceMobilisation {service} />
        </div>
      {/if}

      <div class="rounded-lg border border-gray-02 p-s32 pb-s48">
        <ServiceKeyInformations {service} {servicesOptions} display="sidebar" />
      </div>

      {#if !isModel}
        <div class="rounded-lg border border-gray-02 p-s32 pb-s48 print:hidden">
          <ServiceShare {service} />
        </div>
      {/if}
    </div>
  </div>
</CenteredGrid>

<style lang="postcss">
  .presentation {
    grid-area: presentation;
  }

  .beneficiaries {
    grid-area: beneficiaries;
  }

  .mobilize {
    grid-area: mobilize;
  }

  .sidebar {
    grid-area: sidebar;
  }

  .service-body {
    display: grid;
    grid-template-columns: 1fr;
    column-gap: 6rem;
    row-gap: 2rem;
    grid-template-areas:
      "presentation"
      "sidebar"
      "separator-1"
      "beneficiaries"
      "separator-2"
      "mobilize";
  }

  @screen md {
    .service-body {
      grid-template-columns: 1fr 300px;
      column-gap: 4rem;
      grid-template-areas:
        "presentation sidebar"
        "separator-1 sidebar"
        "beneficiaries sidebar"
        "separator-2 sidebar"
        "mobilize sidebar";
    }
  }
  @screen lg {
    .service-body {
      grid-template-columns: 1fr 375px;
    }
  }
</style>
