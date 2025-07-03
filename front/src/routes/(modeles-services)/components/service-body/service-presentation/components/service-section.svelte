<script lang="ts">
  interface Props {
    title: string;
    children?: import('svelte').Snippet;
  }

  let { title, children }: Props = $props();
</script>

<section class="gap-s24 text-gray-text flex flex-col">
  <h2 class="text-f23 text-france-blue mb-s0 leading-32 font-bold">
    {title}
  </h2>
  {@render children?.()}
</section>
