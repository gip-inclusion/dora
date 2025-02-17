<script lang="ts">
  import Info from "$lib/components/display/info.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";

  interface Props {
    isOpen?: boolean;
  }

  let { isOpen = $bindable(false) }: Props = $props();
</script>

<Modal bind:isOpen title="Suggestion envoyée">
  <Info label="Votre suggestion a bien été envoyée." positiveMood>
    Vos remarques et suggestions ont été transmises aux personnes concernées.
    Merci pour votre participation à l’amélioration de DORA&nbsp;! 🙌
  </Info>
</Modal>
