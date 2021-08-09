<script>
  import Button from "$lib/components/button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import { arrowRightSIcon, arrowLeftCircleIcon } from "$lib/icons.js";
  export let withBack = false;
  export let withForward = false;
  export let withValidate = false;
  export let backlink, forwardlink;

  import { persistAndGo } from "./_nav.js";

  function handleSubmit(evt) {
    persistAndGo(evt, backlink, forwardlink);
  }
</script>

<CenteredGrid class1="sticky w-full p-3 bottom-1 shadow-l bg-white z-50 mt-3">
  <form
    on:submit|preventDefault={handleSubmit}
    class="col-span-full col-start-1 ">
    <div class="flex flex-row gap-6">
      {#if withBack}
        <Button
          name="backward"
          type="submit"
          label="Retour"
          icon={arrowLeftCircleIcon}
          noBackground
          iconOnLeft />
      {/if}
      <div class="flex-grow" />

      <Button
        name="save_draft"
        type="submit"
        label="Enregistrer comme brouillon"
        tertiary />
      {#if withForward}
        <Button
          name="forward"
          type="submit"
          label="Suivant"
          icon={arrowRightSIcon}
          iconOnRight />
      {/if}
      {#if withValidate}
        <Button
          name="validate"
          type="submit"
          label="Publier"
          icon={arrowRightSIcon}
          iconOnRight />
      {/if}
    </div>
  </form>
</CenteredGrid>
