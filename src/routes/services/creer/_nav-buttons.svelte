<script>
  import Button from "$lib/components/button.svelte";

  import { arrowRightSIcon, arrowLeftCircleIcon } from "$lib/icons.js";
  export let withBack = false;
  export let withForward = false;
  export let withPublish = false;
  export let withDraft = false;
  export let onGoBack, onGoForward, onPublish, onSaveDraft;
  export let currentPageIsValid;
</script>

<div class="col-span-full col-start-1 ">
  <div class="flex flex-row gap-6">
    {#if withBack}
      <Button
        on:click={onGoBack}
        name="backward"
        label="Étape précédente"
        icon={arrowLeftCircleIcon}
        noBackground
        iconOnLeft />
    {/if}
    <div class="flex-grow" />
    {#if withDraft}
      <Button
        on:click={onSaveDraft}
        name="save_draft"
        label="Enregistrer comme brouillon"
        tertiary />
    {/if}
    {#if withForward}
      <Button
        on:click={onGoForward}
        name="forward"
        label="Suivant"
        disabled={currentPageIsValid}
        icon={arrowRightSIcon}
        iconOnRight />
    {/if}
    {#if withPublish}
      <Button
        on:click={onPublish}
        name="validate"
        label="Publier"
        disabled={currentPageIsValid}
        icon={arrowRightSIcon}
        iconOnRight />
    {/if}
  </div>
</div>
