<script lang="ts">
  import { fly } from "svelte/transition";

  import BookmarkFillBusiness from "svelte-remix/BookmarkFillBusiness.svelte";
  import BookmarkLineBusiness from "svelte-remix/BookmarkLineBusiness.svelte";
  import CheckLineSystem from "svelte-remix/CheckLineSystem.svelte";
  import FileCopyLineDocument from "svelte-remix/FileCopyLineDocument.svelte";
  import MailLineBusiness from "svelte-remix/MailLineBusiness.svelte";
  import PrinterLineBusiness from "svelte-remix/PrinterLineBusiness.svelte";

  import { browser } from "$app/environment";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import Tooltip from "$lib/components/ui/tooltip.svelte";
  import { token } from "$lib/utils/auth";
  import type { Service } from "$lib/types";

  import SharingModal from "../../components/sharing-modal.svelte";
  import ServiceActionButton from "./service-action-button.svelte";

  export let service: Service;

  const copyLabel = "Copier";
  const printLabel = "Imprimer";
  const shareLabel = "Partager par e-mail";

  let sharingModalIsOpen = false;
  let linkCopied = false;

  function handleCopy() {
    navigator.clipboard.writeText(window.location.href);
    linkCopied = true;
    setTimeout(() => (linkCopied = false), 2000);
  }

  function handlePrint() {
    window.print();
  }

  function handleShare() {
    sharingModalIsOpen = true;
  }

  function handleBookmark(onBookmark: () => void) {
    if (!$token) {
      goto(
        `/auth/connexion?next=${encodeURIComponent(
          $page.url.pathname + $page.url.search
        )}`
      );
      return;
    }
    onBookmark();
  }

  $: isDI = "source" in service;
</script>

<div class="gap-s16 flex">
  <Tooltip>
    <ServiceActionButton ariaLabel={copyLabel} on:click={handleCopy}>
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
    <span slot="content">{copyLabel}</span>
  </Tooltip>
  <Tooltip>
    <ServiceActionButton ariaLabel={printLabel} on:click={handlePrint}>
      <PrinterLineBusiness />
    </ServiceActionButton>
    <span slot="content">{printLabel}</span>
  </Tooltip>
  <Tooltip>
    <ServiceActionButton ariaLabel={shareLabel} on:click={handleShare}>
      <MailLineBusiness />
    </ServiceActionButton>
    <span slot="content">{shareLabel}</span>
  </Tooltip>
  <Bookmarkable slug={service.slug} {isDI} let:onBookmark let:isBookmarked>
    {@const bookmarLabel = isBookmarked
      ? "Retirer de vos favoris"
      : "Ajouter à vos favoris"}
    <Tooltip>
      <ServiceActionButton
        ariaLabel={bookmarLabel}
        on:click={() => handleBookmark(onBookmark)}
      >
        {#if isBookmarked}
          <BookmarkFillBusiness class="text-magenta-cta" />
        {:else}
          <BookmarkLineBusiness />
        {/if}
      </ServiceActionButton>
      <span slot="content">{bookmarLabel}</span>
    </Tooltip>
  </Bookmarkable>
</div>

{#if browser}
  <SharingModal bind:isOpen={sharingModalIsOpen} {service} {isDI} />
{/if}
