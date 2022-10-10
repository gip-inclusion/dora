<script lang="ts">
  import { fly } from "svelte/transition";

  import LinkButton from "$lib/components/link-button.svelte";
  import { CANONICAL_URL, PDF_SERVICE_URL } from "$lib/env";
  import { checkIcon, downloadIcon, linkIcon } from "$lib/icons";

  import type { DashboardService, Service } from "$lib/types";
  import { trackPDFDownload } from "$lib/utils/plausible";

  export let service: Service | DashboardService;
  export let copied = false;

  const serviceLink = `${CANONICAL_URL}/services/${service.slug}`;

  function doCopy() {
    navigator.clipboard.writeText(serviceLink);

    copied = true;
    setTimeout(() => (copied = false), 2000);
  }

  export let pdfUrl = `${PDF_SERVICE_URL}/print/?page=${encodeURIComponent(
    `/services/${service.slug}`
  )}&name=${service.slug}.pdf`;
</script>

<div>
  <h2 class="mb-s32 text-f23">Partager ce service</h2>
  <button
    title="Copier le lien"
    class="relative mb-s12 flex w-full items-center overflow-hidden rounded border border-gray-02 p-s24 pl-s8 text-magenta-cta"
    on:click={doCopy}
  >
    {#if copied}
      <span
        class="absolute h-s24 w-s24 fill-current p-s2"
        transition:fly={{ y: 50, duration: 250 }}
      >
        {@html checkIcon}
      </span>
    {:else}
      <span
        class="absolute h-s24 w-s24 fill-current p-s2"
        transition:fly={{ y: 50, duration: 250 }}
      >
        {@html linkIcon}
      </span>
    {/if}

    <span
      class="absolute left-s40 max-w-[80%] overflow-hidden overflow-ellipsis whitespace-nowrap"
    >
      {serviceLink}
    </span>
  </button>

  <LinkButton
    secondary
    wFull
    icon={downloadIcon}
    label="Télécharger en PDF"
    to={pdfUrl}
    on:click={() => trackPDFDownload(service)}
    nofollow
  />
</div>
