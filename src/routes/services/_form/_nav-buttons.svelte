<script>
  import Button from "$lib/components/button.svelte";

  export let onSaveDraft, onPublish;
</script>

<div class="flex flex-row gap-s12">
  <Button
    on:click={onSaveDraft}
    name="save"
    label="Enregistrer en brouillon"
    secondary
  />

  <Button on:click={onPublish} name="publish" label="Publier" />
</div>
