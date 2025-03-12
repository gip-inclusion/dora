<script lang="ts">
  import type { Service } from "$lib/types";
  import FileCopyLineDocument from "svelte-remix/FileCopyLineDocument.svelte";
  import PrinterLineBusiness from "svelte-remix/PrinterLineBusiness.svelte";
  import MailLineBusiness from "svelte-remix/MailLineBusiness.svelte";
  import BookmarkFillBusiness from "svelte-remix/BookmarkFillBusiness.svelte";
  import BookmarkLineBusiness from "svelte-remix/BookmarkLineBusiness.svelte";
  import ServiceActionButton from "./service-action-button.svelte";
  import Bookmarkable from "$lib/components/hoc/bookmarkable.svelte";
  import { browser } from "$app/environment";
  import { userInfo } from "$lib/utils/auth";
  export let service: Service;

  function handleCopy() {
    navigator.clipboard.writeText(window.location.href);
  }

  function handlePrint() {
    window.print();
  }

  $: isDI = "source" in service;
</script>

<div class="gap-s16 flex">
  <ServiceActionButton ariaLabel="Copier le lien" on:click={handleCopy}>
    <FileCopyLineDocument />
  </ServiceActionButton>
  <ServiceActionButton
    ariaLabel="Imprimer/Exporter en PDF"
    on:click={handlePrint}
  >
    <PrinterLineBusiness />
  </ServiceActionButton>
  <ServiceActionButton ariaLabel="Envoyer par e-mail">
    <MailLineBusiness />
  </ServiceActionButton>
  {#if browser && $userInfo && service.status !== "ARCHIVED"}
    <Bookmarkable slug={service.slug} {isDI} let:onBookmark let:isBookmarked>
      <ServiceActionButton
        ariaLabel={isBookmarked ? "Retirer des favoris" : "Ajouter aux favoris"}
        on:click={onBookmark}
      >
        {#if isBookmarked}
          <BookmarkFillBusiness class="text-magenta-cta" />
        {:else}
          <BookmarkLineBusiness />
        {/if}
      </ServiceActionButton>
    </Bookmarkable>
  {/if}
</div>
