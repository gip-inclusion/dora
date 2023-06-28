<script lang="ts">
  import UserMainActivityForm from "./user-main-activity-form.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import dayjs from "dayjs";

  const USER_MAIN_ACTIVITY_MODAL_KEY = "noUserMainActivityModalUntil";

  let isOpen = false;

  function isMainActivityModalOpen(): boolean {
    const userMainActivityModalUntil = localStorage.getItem(
      USER_MAIN_ACTIVITY_MODAL_KEY
    );
    if (userMainActivityModalUntil === null) {
      return true;
    }

    try {
      return dayjs().isAfter(dayjs(userMainActivityModalUntil));
    } catch (_err) {
      return true;
    }
  }

  function onSuccess() {
    isOpen = false;
  }

  function onClose() {
    localStorage.setItem(
      USER_MAIN_ACTIVITY_MODAL_KEY,
      dayjs().add(10, "hours").toISOString()
    );
    isOpen = false;
  }

  $: isOpen = isMainActivityModalOpen();
</script>

<Modal bind:isOpen title="Dites-nous plus sur vous !" on:close={onClose}>
  <UserMainActivityForm {onSuccess} />
</Modal>
