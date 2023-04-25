<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { CANONICAL_URL, PDF_SERVICE_URL } from "$lib/env";
  import { checkIcon, downloadIcon, linkIcon } from "$lib/icons";
  import type { Service, ShortService } from "$lib/types";
  import { trackPDFDownload } from "$lib/utils/plausible";
  import { fly } from "svelte/transition";

  export let service: Service | ShortService;
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

  {#if service.status === "PUBLISHED"}
    <!-- Le `nofollow` est important ici, on ne veut pas que les robots provoquent la génération des PDFs -->
    <LinkButton
      secondary
      wFull
      icon={downloadIcon}
      label="Télécharger en PDF"
      to={pdfUrl}
      on:click={() => trackPDFDownload(service)}
      nofollow
    />
  {/if}
</div>
