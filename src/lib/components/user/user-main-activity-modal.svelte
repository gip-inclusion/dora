<script lang="ts">
  import UserMainActivityForm from "./user-main-activity-form.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";

  let isOpen = true;

  function onSuccess() {
    isOpen = false;
  }
</script>

<Modal bind:isOpen title="Dites-nous plus sur vous !" canClose={false}>
  <UserMainActivityForm {onSuccess} />
</Modal>
