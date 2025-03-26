<script lang="ts">
  import illustration from "$lib/assets/illustrations/Validation_Orientation_Envoyee.webp";
  import Modal from "$lib/components/hoc/modal.svelte";

  export let isOpen = false;
</script>

<Modal width="small" bind:isOpen title="Vous avez une suggestion ?">
  <div class="text-center">
    <img
      class="mx-auto w-[320px]"
      src={illustration}
      alt=""
      aria-hidden="true"
    />
    <h2 class="text-f17 text-gray-text leading-s24 mb-s4 font-bold">
      Merci pour votre signalement !
    </h2>
    <span class="text-f14 text-gray-text leading-s24">
      La structure concernée sera informée des modifications suggérées.
    </span>
  </div>
</Modal>
