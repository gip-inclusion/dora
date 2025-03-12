<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";
  import ServiceStateUpdateSelect from "$lib/components/specialized/services/service-state-update-select.svelte";
  import SynchronizedIcon from "$lib/components/specialized/services/synchronized-icon.svelte";
  import { copyIcon2 } from "$lib/icons";
  import type { Service, ServicesOptions } from "$lib/types";
  import ServiceActionButtons from "./service-action-buttons.svelte";
  import ServiceUpdateDate from "./service-update-date.svelte";
  import ServiceUpdateButtons from "./service-update-buttons.svelte";
  export let service: Service;
  export let servicesOptions: ServicesOptions;
  export let onRefresh: () => void;
</script>

<div class="hidden print:block">
  <CenteredGrid noPadding>
    <RelativeDateLabel date={service.modificationDate} prefix="Actualisé le" />
  </CenteredGrid>
</div>
<div class="relative print:hidden">
  <CenteredGrid>
    <div class="flex items-center justify-between">
      <ServiceUpdateDate {service} />
      {#if service.canWrite}
        <ServiceUpdateButtons {service} {servicesOptions} {onRefresh} />
      {:else}
        <ServiceActionButtons {service} />
      {/if}
    </div>
  </CenteredGrid>

  {#if !service.canWrite || !service.updateNeeded || service.status !== "PUBLISHED"}
    <div
      class="border-gray-02 m-auto max-w-6xl border border-t-0 border-r-0 border-l-0"
    />
  {/if}

  {#if service.canWrite}
    <CenteredGrid extraClass="w-full" noPadding>
      <div
        class="gap-s24 py-s32 flex w-full flex-col place-content-between items-center sm:flex-row"
      >
        <div>
          <ServiceStateUpdateSelect
            {service}
            {servicesOptions}
            {onRefresh}
            hideLabel={false}
          />
        </div>
        <div class="h-s48 flex items-center md:self-end">
          {#if service.model}
            {#if service.modelChanged}
              <div class="text-f14 text-gray-text flex items-center font-bold">
                <span class="mr-s10"><SynchronizedIcon warning /></span>
                <a href="/services/{service.slug}/editer" class="underline">
                  Mise à jour du modèle disponible
                </a>
              </div>
            {:else}
              <div class="text-f14 text-gray-text flex items-center italic">
                <span class="mr-s10"><SynchronizedIcon /></span>
                <a href="/modeles/{service.model}" class="underline">
                  Synchronisé avec un modèle
                </a>
              </div>
            {/if}
          {:else if !service.useInclusionNumeriqueScheme}
            <LinkButton
              label="Utiliser comme modèle"
              icon={copyIcon2}
              iconOnRight
              noBackground
              hoverUnderline
              to={`/modeles/creer?service=${service.slug}&structure=${service.structure}`}
            />
          {/if}
        </div>
      </div>
    </CenteredGrid>
  {/if}
</div>
