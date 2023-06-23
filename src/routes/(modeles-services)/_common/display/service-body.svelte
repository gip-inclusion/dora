<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";

  import ServiceBeneficiaries from "./service-beneficiaries.svelte";
  import ServiceMobilisation from "./service-mobilisation.svelte";
  import ServiceMobilize from "./service-mobilize.svelte";
  import SmallServiceShare from "./small-service-share.svelte";
  import ServicePresentation from "./service-presentation.svelte";
  import AbTestingSection from "$lib/components/specialized/ab-testing-section.svelte";

  import ServiceKeyInformations from "$lib/components/specialized/services/display/old/service-key-informations.svelte";
  import ServiceShare from "$lib/components/specialized/services/display/old/service-share.svelte";
  import { browser } from "$app/environment";

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

    {#if browser}
      <div class="sidebar flex flex-col gap-y-s24">
        {#if !isModel}
          <div class="sticky top-s32">
            <AbTestingSection
              abTestingName="mobilisation"
              showIfGroups={["mobilisation--fond-bleu"]}
            >
              <div
                class="block rounded-lg border border-gray-02 bg-france-blue p-s24 px-s32 text-white print:hidden"
              >
                <ServiceMobilisation {service} backgroundColor="blue" />
              </div>
            </AbTestingSection>

            <AbTestingSection
              abTestingName="mobilisation"
              showIfGroups={["mobilisation--fond-blanc"]}
            >
              <div class="block rounded-lg p-s24 px-s32 shadow-md print:hidden">
                <ServiceMobilisation {service} />
              </div>
            </AbTestingSection>

            <AbTestingSection
              abTestingName="mobilisation"
              showIfGroups={[
                "mobilisation--fond-bleu",
                "mobilisation--fond-blanc",
              ]}
            >
              {#if !isModel}
                <div class="mt-s24 flex flex-col gap-y-s24">
                  <SmallServiceShare {service} />
                </div>
              {/if}
            </AbTestingSection>
          </div>
        {/if}

        <AbTestingSection
          abTestingName="mobilisation"
          showIfGroups={["mobilisation--ancien-design"]}
        >
          <div
            class="block rounded-lg border border-gray-02 p-s24 px-s32 print:hidden"
          >
            <ServiceMobilisation {service} />
          </div>

          <div class="rounded-lg border border-gray-02 p-s32 pb-s48">
            <ServiceKeyInformations
              {service}
              {servicesOptions}
              display="sidebar"
            />
          </div>

          {#if !isModel}
            <div
              class="rounded-lg border border-gray-02 p-s32 pb-s48 print:hidden"
            >
              <ServiceShare {service} />
            </div>
          {/if}
        </AbTestingSection>
      </div>
    {/if}
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
