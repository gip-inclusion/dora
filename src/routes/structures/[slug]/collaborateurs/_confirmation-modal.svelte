<script>
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Info from "$lib/components/info.svelte";

  import Modal from "$lib/components/modal.svelte";
  export let email;
  export let isOpen = false;
</script>

<Modal bind:isOpen>
  <Fieldset title="Ajouter des collaborateurs" noTopPadding>
    <Info label="Votre demande a été enregistrée" positiveMood>
      Une invitation a été envoyée à l’adresse <strong>{email}</strong>
    </Info>
  </Fieldset>
</Modal>
