<script lang="ts">
  import { getContext } from "svelte";

  interface Props {
    onclick: () => void;
  }

  let { onclick }: Props = $props();

  const showFeedbackModal = getContext("showFeedbackModal");
</script>

{#if showFeedbackModal}
  <div>
    <button class="text-gray-text underline" {onclick}
      >Signalez-nous toute erreur ou suggestion de modification.</button
    >
  </div>
{/if}
