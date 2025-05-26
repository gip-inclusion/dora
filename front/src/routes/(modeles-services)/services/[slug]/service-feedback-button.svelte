<script lang="ts">
  import { getContext } from "svelte";

  const showFeedbackModal = getContext("showFeedbackModal");
</script>

{#if showFeedbackModal}
  <div>
    <button class="text-gray-text underline" on:click
      >Signalez-nous toute erreur ou suggestion de modification.</button
    >
  </div>
{/if}
