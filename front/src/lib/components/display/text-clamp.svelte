<script lang="ts">
  import { randomId } from "$lib/utils/random";

  import Button from "./button.svelte";
  import MarkdownRenderer from "./markdown-renderer.svelte";

  interface Props {
    text: string;
    // hauteur du texte visible une fois replié
    clampedHeight?: number;
  }

  let { text, clampedHeight = 112 }: Props = $props();

  const id = `text-clamp-${randomId()}`;

  let showAll = $state(false);
  let height: number = $state(0);

  function toggle() {
    showAll = !showAll;
  }

  let textIsTooLong = $derived(height > clampedHeight);
  let isClamped = $derived(!showAll && textIsTooLong);
  let label = $derived(showAll ? "Réduire" : "Lire la suite");
</script>

<div class="hidden print:inline">
  <div class="prose mb-s24"><MarkdownRenderer content={text} /></div>
</div>
<div class="print:hidden">
  <div
    {id}
    class="mb-s6 relative overflow-hidden"
    style:height={isClamped ? `${clampedHeight}px` : undefined}
  >
    <div class="prose mb-s12" bind:clientHeight={height}>
      <MarkdownRenderer content={text} />
    </div>
    {#if isClamped}
      <!-- le dégradé ne couvre que la dernière ligne, pas tout le bloc replié -->
      <div
        class="bottom-s0 left-s0 h-s48 absolute w-full bg-gradient-to-b from-transparent to-white"
      ></div>
    {/if}
  </div>

  {#if textIsTooLong}
    <Button
      ariaAttributes={{
        "aria-expanded": showAll,
        "aria-controls": id,
      }}
      {label}
      onclick={toggle}
      noBackground
      small
      noPadding
    />
  {/if}
</div>
