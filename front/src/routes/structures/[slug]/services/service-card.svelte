<script lang="ts">
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import FavoriteIcon from "$lib/components/specialized/favorite-icon.svelte";
  import ServiceStateUpdateSelect from "$lib/components/specialized/services/service-state-update-select.svelte";
  import SynchronizedIcon from "$lib/components/specialized/services/synchronized-icon.svelte";
  import UpdateNeededIcon from "$lib/components/specialized/services/update-needed-icon.svelte";
  import type { ServicesOptions, ShortService } from "$lib/types";
  import ServiceButtonMenu from "./service-button-menu.svelte";

  interface Props {
    service: ShortService;
    servicesOptions: ServicesOptions;
    readOnly?: boolean;
    onRefresh: () => void;
  }

  let {
    service,
    servicesOptions,
    readOnly = true,
    onRefresh,
  }: Props = $props();
</script>

<Bookmarkable slug={service.slug}>
  {#snippet children({ onBookmark, isBookmarked })}
    <div
      class="relative flex flex-col justify-between rounded-lg bg-white shadow-md"
    >
      <div class="g row mb-s32 p-s24 rounded-t-md">
        {#if !readOnly}
          <div class="mb-s24 flex items-center justify-between">
            <div class="relative z-10">
              <ServiceStateUpdateSelect
                {service}
                {servicesOptions}
                {onRefresh}
                fullWidth
              />
            </div>

            {#if service.status !== "SUGGESTION" && service.status !== "ARCHIVED"}
              <div class="relative z-10">
                <ServiceButtonMenu {service} {servicesOptions} {onRefresh} />
              </div>
            {/if}
          </div>
        {/if}

        <div class="mb-s24 gap-s10 flex justify-between">
          <h3 class="mb-s0 leading-28">
            <a
              class="full-card-link text-f19 text-france-blue font-bold hover:underline"
              href="/services/{service.slug}">{service.name}</a
            >
          </h3>
          {#if readOnly}
            <div class="top-s6 relative flex">
              <FavoriteIcon on:click={onBookmark} active={isBookmarked} />
            </div>
          {/if}
        </div>

        {#if service.diffusionZoneDetailsDisplay}
          <div class="mb-s8 text-france-blue flex items-center">
            Périmètre&nbsp;:&nbsp;<strong
              >{service.diffusionZoneDetailsDisplay}</strong
            >
          </div>
        {/if}
        {#if !readOnly && service.city && service.locationKinds.includes("en-presentiel")}
          <div class="mb-s8 text-france-blue flex items-center">
            Lieu d’accueil&nbsp;:&nbsp;<strong>{service.city}</strong>
          </div>
        {/if}
      </div>

      <div
        class="gap-s8 border-t-gray-03 px-s20 py-s12 flex min-h-[100px] flex-col justify-center border-t"
      >
        <div class="flex items-center">
          <span class="mr-s8">
            <UpdateNeededIcon updateNeeded={service.updateNeeded} small />
          </span>
          <div class="text-f14">
            <RelativeDateLabel
              date={service.modificationDate}
              prefix="Actualisé"
              bold={service.updateNeeded}
            />
          </div>
        </div>

        {#if !readOnly && service.model}
          <div class="text-f14 flex items-center">
            {#if service.modelChanged}
              <span class="mr-s8"><SynchronizedIcon warning small /></span>
              <a
                href="/services/{service.slug}/editer"
                class="relative hover:underline"
              >
                <span class="font-bold">Mise à jour du modèle disponible</span>
              </a>
            {:else}
              <span class="mr-s8"><SynchronizedIcon small /></span>
              <span class="text-gray-text italic">
                Synchronisé avec un modèle
              </span>
            {/if}
          </div>
        {/if}
      </div>
    </div>
  {/snippet}
</Bookmarkable>
