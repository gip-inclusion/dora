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
  import type { Service } from "$lib/types";
  import { token } from "$lib/utils/auth";

  import SharingModal from "../../components/sharing-modal.svelte";
  import ServiceActionButton from "./service-action-button.svelte";

  export let service: Service;

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
  <ServiceActionButton ariaLabel="Copier" on:click={handleCopy}>
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
  <ServiceActionButton ariaLabel="Imprimer" on:click={handlePrint}>
    <PrinterLineBusiness />
  </ServiceActionButton>
  <ServiceActionButton ariaLabel="Partager par e-mail" on:click={handleShare}>
    <MailLineBusiness />
  </ServiceActionButton>
  <Bookmarkable slug={service.slug} {isDI} let:onBookmark let:isBookmarked>
    <ServiceActionButton
      ariaLabel={isBookmarked
        ? "Retirer de vos favoris"
        : "Ajouter à vos favoris"}
      on:click={() => handleBookmark(onBookmark)}
    >
      {#if isBookmarked}
        <BookmarkFillBusiness class="text-magenta-cta" />
      {:else}
        <BookmarkLineBusiness />
      {/if}
    </ServiceActionButton>
  </Bookmarkable>
</div>

{#if browser}
  <SharingModal bind:isOpen={sharingModalIsOpen} {service} {isDI} />
{/if}
