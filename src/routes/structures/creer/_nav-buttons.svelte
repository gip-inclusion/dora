<script>
  import Button from "$lib/components/button.svelte";
  import { arrowRightIcon, arrowLeftIcon } from "$lib/icons.js";
  export let withBack = false;
  export let withForward = false;
  export let withValidate = false;
</script>

<div class="flex flex-row justify-center max-w-xl gap-6 p-8 mx-auto mt-8">
  {#if withBack}
    <Button
      name="backward"
      type="submit"
      label="Précédent"
      secondary={withForward || withValidate}
      icon={arrowLeftIcon}
      iconOnLeft />
  {/if}
  {#if withForward}
    <Button
      name="forward"
      type="submit"
      label="Suivant"
      icon={arrowRightIcon}
      iconOnRight />
  {/if}
  {#if withValidate}
    <Button
      name="validate"
      type="submit"
      label="Valider"
      icon={arrowRightIcon}
      iconOnRight />
  {/if}
</div>
