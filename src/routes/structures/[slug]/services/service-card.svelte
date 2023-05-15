<script lang="ts">
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import FavoriteIcon from "$lib/components/specialized/favorite-icon.svelte";
  import ServiceStateUpdateSelect from "$lib/components/specialized/services/service-state-update-select.svelte";
  import SynchronizedIcon from "$lib/components/specialized/services/synchronized-icon.svelte";
  import UpdateStatusIcon from "$lib/components/specialized/services/update-status-icon.svelte";
  import type { ServicesOptions, ShortService } from "$lib/types";
  import ServiceButtonMenu from "./service-button-menu.svelte";

  export let service: ShortService;
  export let servicesOptions: ServicesOptions;
  export let readOnly = true;
  export let onRefresh: () => void;
</script>

<Bookmarkable slug={service.slug} let:onBookmark let:isBookmarked>
  <div
    class="relative flex flex-col justify-between rounded-md bg-white shadow-md"
  >
    <div class="g row mb-s32 rounded-t-md p-s24">
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

      <div class="mb-s24 flex justify-between gap-s10">
        <h3 class="mb-s0 leading-28">
          <a
            class="full-card-link text-f19 font-bold text-france-blue hover:underline"
            href="/services/{service.slug}">{service.name}</a
          >
        </h3>
        {#if readOnly}
          <div class="relative top-s6 flex">
            <FavoriteIcon on:click={onBookmark} active={isBookmarked} small />
          </div>
        {/if}
      </div>

      {#if service.diffusionZoneDetailsDisplay}
        <div class="mb-s8 flex items-center text-france-blue">
          Périmètre&nbsp;:&nbsp;<strong
            >{service.diffusionZoneDetailsDisplay}</strong
          >
        </div>
      {/if}
      {#if !readOnly && service.city && service.locationKinds.includes("en-presentiel")}
        <div class="mb-s8 flex items-center text-france-blue">
          Lieu d'accueil&nbsp;:&nbsp;<strong>{service.city}</strong>
        </div>
      {/if}
    </div>

    <div
      class="flex min-h-[100px] flex-col justify-center gap-s10 border-t border-t-gray-03 py-s12 px-s20"
    >
      <div class="flex items-center text-f14 text-gray-text">
        {#if service.status !== "PUBLISHED" || service.updateStatus === "NOT_NEEDED"}
          <span class="mr-s8">
            <UpdateStatusIcon updateStatus="NOT_NEEDED" small />
          </span>
          <RelativeDateLabel
            date={service.modificationDate}
            prefix="Actualisé"
          />
        {:else if service.updateStatus === "NEEDED"}
          <span class="mr-s8">
            <UpdateStatusIcon updateStatus="NEEDED" small />
          </span>
          <span class="font-bold">Actualisation conseillée</span>
        {:else if service.updateStatus === "REQUIRED"}
          <span class="mr-s8">
            <UpdateStatusIcon updateStatus="REQUIRED" small />
          </span>
          <strong>Actualisation requise</strong>
        {/if}
      </div>

      {#if !readOnly && service.model}
        <div class="flex items-center text-f14">
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
            <span class="italic text-gray-text">
              Synchronisé avec un modèle
            </span>
          {/if}
        </div>
      {/if}
    </div>
  </div>
</Bookmarkable>

<style lang="postcss">
  /*
  * Link is on <h2> but we want all the card clickable (in an accessible way)
  * Source: http://inclusive-components.design/cards/
  */
  /* .full-card-link::after {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
  } */
</style>
