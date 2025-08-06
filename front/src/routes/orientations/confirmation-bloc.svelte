<script lang="ts">
  import FlashlightLineWeather from "svelte-remix/FlashlightLineWeather.svelte";

  import illustration from "$lib/assets/illustrations/illu-favs.svg";

  interface Props {
    title: any;
    subtitle?: string;
    withThunder?: boolean;
  }

  let { title, subtitle = "", withThunder = false }: Props = $props();
</script>

<div class="mb-s24 gap-s24 flex flex-col items-center">
  {#if withThunder}
    <div class="mt-s10 h-s24 w-s24 mx-auto">
      <FlashlightLineWeather />
    </div>
  {/if}

  <h1 class="m-s0 text-f32 text-gray-text">{title}</h1>

  {#if subtitle}
    <p class="m-s0 text-f14 text-gray-text">
      {subtitle}
    </p>
  {/if}

  <img src={illustration} alt="" />
</div>
