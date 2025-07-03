<script lang="ts">
  interface Props {
    children?: import('svelte').Snippet;
  }

  let { children }: Props = $props();
</script>

<ul class="space-y-s2 list-inside list-disc">
  {@render children?.()}
</ul>
