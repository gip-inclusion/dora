<script lang="ts">
  interface Props {
    children?: import('svelte').Snippet;
  }

  let { children }: Props = $props();
</script>

<div
  class="bold bg-magenta-dark px-s8 text-f14 inline-block w-fit self-center rounded-full pt-[1px] pb-[3px] leading-[18px] text-white"
>
  {@render children?.()}
</div>
