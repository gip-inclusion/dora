<script>
  import Button from "$lib/components/button.svelte";
  import RadioButtons from "$lib/components/forms/radio-buttons.svelte";

  export let onSave, service;
</script>

<div class="col-span-full py-s24">
  <div class="flex flex-row gap-s12">
    <div class="p-s12">
      <RadioButtons
        inline
        bind:group={service.isDraft}
        choices={[
          { label: "Brouillon", value: true },
          { label: "Publié", value: false },
        ]}
      />
    </div>
    <Button on:click={onSave} name="validate" label="Enregistrer" />
  </div>
</div>
