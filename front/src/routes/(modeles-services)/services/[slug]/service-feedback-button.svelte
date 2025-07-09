<script lang="ts">
  import { createBubbler } from "svelte/legacy";

  const bubble = createBubbler();
  import { getContext } from "svelte";

  const showFeedbackModal = getContext("showFeedbackModal");
</script>

{#if showFeedbackModal}
  <div>
    <button class="text-gray-text underline" onclick={bubble("click")}
      >Signalez-nous toute erreur ou suggestion de modification.</button
    >
  </div>
{/if}
