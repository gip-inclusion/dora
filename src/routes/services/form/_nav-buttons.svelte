<script>
  import Button from "$lib/components/button.svelte";

  import { arrowRightSIcon, arrowLeftCircleIcon, eyeIcon } from "$lib/icons.js";
  export let withBack = false;
  export let withForward = false;
  export let withPublish = false;
  export let withDraft = false;
  export let withPreview = false;
  export let isDraft;
  export let onGoBack, onGoForward, onPublish, onModify, onSaveDraft, onPreview;
  export let currentPageIsValid;
  export let flashSaveDraftButton = false;
</script>

<div class="col-span-full col-start-1">
  <div class="flex flex-row gap-s48">
    {#if withBack}
      <Button
        on:click={onGoBack}
        name="backward"
        label="Étape précédente"
        icon={arrowLeftCircleIcon}
        noBackground
        iconOnLeft
      />
    {/if}
    <div class="grow" />
    {#if withDraft}
      <Button
        on:click={onSaveDraft}
        flashSuccess={flashSaveDraftButton}
        name="save_draft"
        label={flashSaveDraftButton
          ? "Enregistré !"
          : "Enregistrer comme brouillon"}
        tertiary
      />
    {/if}
    {#if withForward}
      <Button
        on:click={onGoForward}
        name="forward"
        label="Suivant"
        disabled={currentPageIsValid}
        icon={arrowRightSIcon}
        iconOnRight
      />
    {/if}
    {#if withPreview}
      <Button
        on:click={onPreview}
        name="preview"
        label="Prévisualiser"
        disabled={currentPageIsValid}
        icon={eyeIcon}
        iconOnRight
      />
    {/if}
    {#if withPublish}
      <Button
        on:click={isDraft ? onPublish : onModify}
        name="validate"
        label={isDraft ? "Publier" : "Modifier"}
        disabled={currentPageIsValid}
        icon={arrowRightSIcon}
        iconOnRight
      />
    {/if}
  </div>
</div>
