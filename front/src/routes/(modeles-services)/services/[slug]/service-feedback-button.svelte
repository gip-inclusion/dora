<script lang="ts">
  import { getContext } from "svelte";

  import type { ShowFeedbackModalContext } from "./+page.svelte";

  interface Props {
    onclick: () => void;
  }

  let { onclick }: Props = $props();

  const showFeedbackModal =
    getContext<ShowFeedbackModalContext>("showFeedbackModal");
</script>

{#if showFeedbackModal && showFeedbackModal()}
  <div>
    <button class="text-gray-text underline" {onclick}
      >Signalez-nous toute erreur ou suggestion de modification.</button
    >
  </div>
{/if}
