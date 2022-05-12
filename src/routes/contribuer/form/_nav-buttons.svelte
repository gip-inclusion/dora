<script>
  import Button from "$lib/components/button.svelte";

  export let onPublish;
  export let currentPageIsValid;
</script>

<div class="col-span-full py-s24">
  <Button
    on:click={onPublish}
    name="validate"
    label="Envoyer la contribution"
    disabled={!currentPageIsValid}
  />
</div>
