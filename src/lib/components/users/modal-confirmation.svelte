<script>
  import Info from "$lib/components/info.svelte";
  import Modal from "$lib/components/modal.svelte";

  export let email;
  export let isOpen = false;
</script>

<Modal bind:isOpen title="Demande envoyée">
  <Info label="Merci" positiveMood>
    Une invitation a été envoyée à l’adresse <strong>{email}</strong>
  </Info>
</Modal>
