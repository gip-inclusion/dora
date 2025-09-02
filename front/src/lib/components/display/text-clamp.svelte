<script lang="ts">
  import { randomId } from "$lib/utils/random";

  import Button from "./button.svelte";
  import MarkdownRenderer from "./markdown-renderer.svelte";

  interface Props {
    text: string;
  }

  let { text }: Props = $props();

  const defaultHeight = 200;
  const id = `text-clamp-${randomId()}`;

  let showAll = $state(false);
  let height: number = $state(0);

  function toggle() {
    showAll = !showAll;
  }

  let textIsTooLong = $derived(height + 100 > defaultHeight);
  let label = $derived(showAll ? "Réduire" : "Lire la suite");
</script>

<div class="hidden print:inline">
  <div class="prose mb-s24"><MarkdownRenderer content={text} /></div>
</div>
<div class="print:hidden">
  <div {id} class:h-s112={!showAll} class="mb-s6 relative overflow-hidden">
    <div class="prose mb-s12" bind:clientHeight={height}>
      <MarkdownRenderer content={text} />
    </div>
    {#if !showAll && textIsTooLong}
      <div
        class="bottom-s0 left-s0 h-s112 absolute w-full bg-gradient-to-b from-transparent to-white"
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
