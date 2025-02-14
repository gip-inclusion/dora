<script lang="ts">
  import Info from "$lib/components/display/info.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";

  interface Props {
    email: any;
    isOpen?: boolean;
  }

  let { email, isOpen = $bindable(false) }: Props = $props();
</script>

<Modal bind:isOpen title="Demande envoyée">
  <Info label="Merci" positiveMood>
    Une invitation a été envoyée à l’adresse <strong>{email}</strong>
  </Info>
</Modal>
