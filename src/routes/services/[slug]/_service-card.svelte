<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import AccessBox from "./_access-box.svelte";
  import ModalitiesBox from "./_modalities-box.svelte";
  import OrientationBox from "./_orientation-box.svelte";
  import ServiceHeader from "./_service-header.svelte";
  import ServicePresentation from "./_service-presentation.svelte";
  import { shortenString } from "$lib/utils";
  import Tag from "$lib/components/tag.svelte";
  import Toolbar from "./_toolbar.svelte";
  import AdminNotice from "$lib/components/structures/admin-notice.svelte";
  import { getService } from "$lib/services";
  import { browser } from "$app/env";

  export let service;
  export let isPreview = false;

  async function handleRefresh() {
    service = await getService(service.slug);
  }
</script>

<CenteredGrid --col-bg="var(--col-gray-00)">
  <ServiceHeader {service} />
</CenteredGrid>

<CenteredGrid bordertop --col-content-bg="var(--col-bg)">
  <div class="noprint mb-s24">
    {#if browser && !isPreview}
      <Toolbar {service} onRefresh={handleRefresh} />
    {/if}
  </div>

  <div class="flex flex-col gap-s24 lg:flex-row">
    <div class="lg:w-2/3">
      <p class="text-f18"><strong>{service.shortDesc}</strong></p>
      <p class="text-f12 text-gray-text-alt">
        {service.kindsDisplay.join(", ")}
      </p>
      <div class="mb-s24">
        {#if service.isCumulative}
          <Tag bgColorClass="bg-info" textColorClass="text-white"
            >Service cumulable</Tag
          >
        {:else}
          <Tag bgColorClass="bg-warning" textColorClass="text-white"
            >Service non cumulable</Tag
          >
        {/if}
        {#if service.hasFee}
          <Tag bgColorClass="bg-warning" textColorClass="text-white"
            >Frais à charge du bénéficiaire</Tag
          >
        {/if}
        {#if service.locationKinds.includes("a-distance")}
          <Tag bgColorClass="bg-info" textColorClass="text-white"
            >À distance</Tag
          >
        {/if}
      </div>
    </div>

    <div class="lg:w-1/3">
      {#if service.locationKinds.length}
        {#if service.locationKinds.includes("en-presentiel")}
          <h4>En présentiel</h4>
          <p class="pb-s16 text-f14">
            {service.address1}<br />
            {#if service.address2}{service.address2}<br />{/if}
            {service.postalCode}
            {service.city}
          </p>
        {/if}
        {#if service.locationKinds.includes("a-distance")}
          <strong>À distance</strong>
          <p class="pb-s16 text-f14">
            <a target="_blank" rel="noopener nofollow" href={service.remoteUrl}
              >{shortenString(service.remoteUrl, 35)}</a
            >
          </p>
        {/if}
      {/if}

      {#if service.recurrence}
        <h4>Fréquence et horaires</h4>
        <p class="text-f14">{service.recurrence}</p>
      {/if}

      {#if !isPreview && !service.structureInfo.hasAdmin}
        <div class="noprint mb-s24">
          <AdminNotice structure={service.structureInfo} />
        </div>
      {/if}
    </div>
  </div>

  <div class="break-word flex flex-col gap-s24 lg:flex-row">
    <div class="lg:w-2/3">
      <div class="mb-s48 flex flex-col gap-s32 lg:flex-row">
        <div class="flex-1">
          <AccessBox {service} />
        </div>
        <div class="flex-1">
          <ModalitiesBox {service} />
        </div>
      </div>
    </div>

    <div class="lg:w-1/3">
      <OrientationBox {service} />
    </div>
  </div>

  {#if service.fullDesc}
    <div class="mb-s48 lg:w-2/3">
      <ServicePresentation {service} />
    </div>
  {/if}
</CenteredGrid>
