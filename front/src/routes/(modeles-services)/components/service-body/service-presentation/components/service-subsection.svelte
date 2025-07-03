<script lang="ts">
  interface Props {
    title: string;
    children?: import('svelte').Snippet;
  }

  let { title, children }: Props = $props();
</script>

<section>
  <h3 class="text-f17 leading-s24 text-gray-dark mb-s8 font-bold">
    {title}
  </h3>
  {@render children?.()}
</section>
