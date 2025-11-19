<script lang="ts">
  import illuRecenser from "$lib/assets/illustrations/illu-recenser.svg";
  import type { Snippet } from "svelte";

  interface Props {
    title: string;
    text: string;
    children: Snippet;
  }

  const { title, text, children }: Props = $props();
</script>

<div class="flex flex-row justify-center border-1 border-dashed">
  <div class="flex flex-col items-center">
    <h2>{title}</h2>
    <h4>
      {text}
    </h4>
    <div class="gap-s32 flex flex-row justify-center">
      {@render children()}
    </div>
  </div>
  <img src={illuRecenser} alt="" class="mb-s16 w-full" />
</div>
