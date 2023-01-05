<script lang="ts">
  import Button from "$lib/components/display/button.svelte";

  export let onPublish;
  export let currentPageIsValid;
</script>

<Button
  on:click={onPublish}
  name="validate"
  label="Envoyer la contribution"
  disabled={!currentPageIsValid}
/>
