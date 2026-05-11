<script lang="ts">
  import { fly } from "svelte/transition";

  import BookmarkFillBusiness from "svelte-remix/BookmarkFillBusiness.svelte";
  import BookmarkLineBusiness from "svelte-remix/BookmarkLineBusiness.svelte";
  import CheckLineSystem from "svelte-remix/CheckLineSystem.svelte";
  import FileCopyLineDocument from "svelte-remix/FileCopyLineDocument.svelte";
  import MailLineBusiness from "svelte-remix/MailLineBusiness.svelte";
  import PrinterLineBusiness from "svelte-remix/PrinterLineBusiness.svelte";

  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import Tooltip from "$lib/components/ui/tooltip.svelte";
  import { isAuthenticated } from "$lib/utils/auth";
  import { buildServiceShareMailto } from "$lib/utils/service-share-mailto";
  import type { Service } from "$lib/types";

  import ServiceActionButton from "./service-action-button.svelte";
  import { trackMatomoEvent } from "$lib/utils/matomo";

  interface Props {
    service: Service;
  }

  let { service }: Props = $props();

  const copyLabel = "Copier";
  const printLabel = "Imprimer";
  const shareLabel = "Partager par e-mail";

  let linkCopied = $state(false);

  function handleCopy() {
    navigator.clipboard.writeText(window.location.href);
    linkCopied = true;
    setTimeout(() => (linkCopied = false), 2000);
  }

  function handlePrint() {
    window.print();
  }

  function handleBookmark(onBookmark: () => void) {
    if (!isAuthenticated()) {
      goto(
        `/auth/connexion?next=${encodeURIComponent(
          $page.url.pathname + $page.url.search
        )}`
      );
      return;
    }
    onBookmark();
  }

  let isDI = $derived("source" in service);
  let shareMailtoHref = $derived(buildServiceShareMailto(service, isDI));

  function handleShareClick() {
    trackMatomoEvent({
      category: "Page Service",
      action: "Clic Bouton Partager cette Fiche",
      name: $page.url.pathname,
    });
  }
</script>

<div class="gap-s16 flex">
  <Tooltip>
    <ServiceActionButton ariaLabel={copyLabel} onclick={handleCopy}>
      <div class="w-s24 h-s24 relative">
        {#if linkCopied}
          <div class="absolute" transition:fly={{ y: 50, duration: 500 }}>
            <CheckLineSystem />
          </div>
        {:else}
          <div class="absolute" transition:fly={{ y: 50, duration: 500 }}>
            <FileCopyLineDocument />
          </div>
        {/if}
      </div>
    </ServiceActionButton>
    {#snippet content()}
      <span>{copyLabel}</span>
    {/snippet}
  </Tooltip>
  <Tooltip>
    <ServiceActionButton ariaLabel={printLabel} onclick={handlePrint}>
      <PrinterLineBusiness />
    </ServiceActionButton>
    {#snippet content()}
      <span>{printLabel}</span>
    {/snippet}
  </Tooltip>
  <Tooltip>
    <ServiceActionButton
      ariaLabel={shareLabel}
      href={shareMailtoHref}
      onclick={handleShareClick}
    >
      <MailLineBusiness />
    </ServiceActionButton>
    {#snippet content()}
      <span>{shareLabel}</span>
    {/snippet}
  </Tooltip>
  <Bookmarkable slug={service.slug} {isDI}>
    {#snippet children({ onBookmark, isBookmarked })}
      {@const bookmarLabel = isBookmarked
        ? "Retirer de vos favoris"
        : "Ajouter à vos favoris"}
      <Tooltip>
        <ServiceActionButton
          ariaLabel={bookmarLabel}
          onclick={() => handleBookmark(onBookmark)}
        >
          {#if isBookmarked}
            <BookmarkFillBusiness class="text-magenta-cta" />
          {:else}
            <BookmarkLineBusiness />
          {/if}
        </ServiceActionButton>
        {#snippet content()}
          <span>{bookmarLabel}</span>
        {/snippet}
      </Tooltip>
    {/snippet}
  </Bookmarkable>
</div>
