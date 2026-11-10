<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    /** Titre affiché au-dessus de la carte */
    title?: string;
    /** Sépare chaque enfant direct par un filet horizontal */
    divided?: boolean;
    children?: Snippet;
  }

  let { title, divided = false, children }: Props = $props();

  const baseClass =
    "border-gray-02 p-s32 text-f16 text-gray-text [&_p]:mb-s0 [&_p]:text-f16 flex flex-col rounded-2xl border leading-24 [&_p]:leading-24";

  const dividedClass =
    "gap-s32 divide-gray-01 divide-y [&>*:not(:last-child)]:pb-s32";

  let cardClass = $derived(
    `${baseClass} ${divided ? dividedClass : "gap-s24"}`
  );
</script>

<section>
  {#if title}
    <h2 class="text-f23 text-france-blue mb-s16 leading-32 font-bold">
      {title}
    </h2>
  {/if}

  <div class={cardClass}>
    {@render children?.()}
  </div>
</section>
