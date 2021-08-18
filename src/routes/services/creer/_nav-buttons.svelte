<script>
  import Button from "$lib/components/button.svelte";

  import { arrowRightSIcon, arrowLeftCircleIcon } from "$lib/icons.js";
  export let withBack = false;
  export let withForward = false;
  export let withValidate = false;
  export let withDraft = false;
  export let currentPageIsValid;
</script>

<div class="col-span-full col-start-1 ">
  <div class="flex flex-row gap-6">
    {#if withBack}
      <Button
        name="backward"
        type="submit"
        label="Étape précédente"
        icon={arrowLeftCircleIcon}
        noBackground
        iconOnLeft />
    {/if}
    <div class="flex-grow" />
    {#if withDraft}
      <Button
        name="save_draft"
        type="submit"
        label="Enregistrer comme brouillon"
        tertiary />
    {/if}
    {#if withForward}
      <Button
        name="forward"
        type="submit"
        label="Suivant"
        disabled={currentPageIsValid}
        icon={arrowRightSIcon}
        iconOnRight />
    {/if}
    {#if withValidate}
      <Button
        name="validate"
        type="submit"
        label="Publier"
        disabled={currentPageIsValid}
        icon={arrowRightSIcon}
        iconOnRight />
    {/if}
  </div>
</div>
