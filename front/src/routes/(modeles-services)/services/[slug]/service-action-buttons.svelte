<script lang="ts">
  import BookmarkFillBusiness from "svelte-remix/BookmarkFillBusiness.svelte";
  import BookmarkLineBusiness from "svelte-remix/BookmarkLineBusiness.svelte";
  import FileCopyLineDocument from "svelte-remix/FileCopyLineDocument.svelte";
  import MailLineBusiness from "svelte-remix/MailLineBusiness.svelte";
  import PrinterLineBusiness from "svelte-remix/PrinterLineBusiness.svelte";

  import { browser } from "$app/environment";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import type { Service } from "$lib/types";
  import { token } from "$lib/utils/auth";

  import SharingModal from "../../_common/display/modals/sharing-modal.svelte";
  import ServiceActionButton from "./service-action-button.svelte";

  export let service: Service;

  let sharingModalIsOpen = false;

  function handleCopy() {
    navigator.clipboard.writeText(window.location.href);
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
    <FileCopyLineDocument />
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
