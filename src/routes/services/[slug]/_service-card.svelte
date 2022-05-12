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

<CenteredGrid --col-bg="var(--col-france-blue)">
  <ServiceHeader {service} />
</CenteredGrid>

<CenteredGrid
  roundedTop
  --col-under-bg="var(--col-france-blue)"
  --col-content-bg="var(--col-bg)"
  topPadded
>
  <div class="noprint col-span-full h-s40">
    {#if browser && !isPreview}
      <Toolbar {service} onRefresh={handleRefresh} />
    {/if}
  </div>

  <div class="col-span-full flex flex-col gap-s24 lg:flex-row-reverse">
    <div class="lg:w-1/3">
      {#if service.locationKinds.length}
        {#if service.locationKinds.includes("en-presentiel")}
          <p class="pb-s16 text-f14">
            {service.address1}<br />
            {#if service.address2}{service.address2}<br />{/if}
            {service.postalCode}
            {service.city}
          </p>
        {/if}
        {#if service.locationKinds.includes("a-distance")}
          <p class="pb-s16 text-f14">
            <a target="_blank" rel="noopener nofollow" href={service.remoteUrl}
              >{shortenString(service.remoteUrl, 35)}</a
            >
          </p>
        {/if}
      {/if}

      {#if service.recurrence}
        <p class="text-f14">{service.recurrence}</p>
      {/if}

      {#if !isPreview && !service.structureInfo.hasAdmin}
        <div class="noprint mb-s24">
          <AdminNotice structure={service.structureInfo} />
        </div>
      {/if}
    </div>
    <div class="lg:w-2/3">
      <p class="text-f18"><strong>{service.shortDesc}</strong></p>
      <p class="list-inside list-disc text-f12 text-gray-text-alt">
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
  </div>

  <div class="col-span-full flex flex-col gap-s24 lg:flex-row-reverse">
    <div class="lg:w-1/3">
      <OrientationBox {service} />
    </div>
    <div class="lg:w-2/3">
      <div class="mb-s48 flex flex-col gap-s32 lg:flex-row">
        <div class="flex-1"><AccessBox {service} /></div>
        <div class="flex-1"><ModalitiesBox {service} /></div>
      </div>
      <div class="mb-s48"><ServicePresentation {service} /></div>
    </div>
  </div>
</CenteredGrid>
