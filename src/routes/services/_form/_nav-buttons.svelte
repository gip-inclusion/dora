<script>
  import Button from "$lib/components/button.svelte";

  export let onPublish, onSaveDraft;
  export let isValid;
</script>

<div class="col-span-full py-s24">
  <div class="flex flex-row gap-s12">
    <Button
      on:click={onSaveDraft}
      name="save_draft"
      label="Enregistrer en brouillon"
      secondary
    />

    <Button
      on:click={onPublish}
      name="validate"
      label="Enregistrer et publier"
      disabled={!isValid}
      iconOnRight
    />
  </div>
</div>
