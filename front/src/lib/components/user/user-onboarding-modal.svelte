<script lang="ts">
  import UserOnboardingForm from "./user-onboarding-form.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";

  let isOpen = true;

  function onSuccess() {
    isOpen = false;
  }
</script>

<Modal
  bind:isOpen
  title="Dites-nous en plus sur vous !"
  subtitle="Pour nous permettre de mieux vous connaître et de répondre précisément à vos besoins."
  width="medium"
  canClose={false}
>
  <UserOnboardingForm {onSuccess} />
</Modal>
