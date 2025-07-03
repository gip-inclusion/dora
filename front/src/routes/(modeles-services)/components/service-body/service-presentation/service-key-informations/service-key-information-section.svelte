<script lang="ts">
  import type { ComponentType } from "svelte";

  interface Props {
    icon: ComponentType;
    title: string;
    children?: import('svelte').Snippet;
  }

  let { icon, title, children }: Props = $props();

  const SvelteComponent = $derived(icon);
</script>

<section>
  <div class="gap-s8 flex">
    <div class="text-france-blue flex-shrink-0">
      <SvelteComponent />
    </div>
    <div class="flex-grow">
      <h3 class="text-f17 text-france-blue mb-s8 leading-24">
        {title}
      </h3>
      {@render children?.()}
    </div>
  </div>
</section>
