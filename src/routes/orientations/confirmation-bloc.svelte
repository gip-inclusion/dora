<script>
  import illustration from "$lib/assets/illustrations/illu-favs.svg";
  import { flashLightIcon } from "$lib/icons";

  export let title;
  export let subtitle = "";
  export let withThunder = false;
</script>

<div class="mb-s24 flex flex-col items-center gap-s24">
  {#if withThunder}
    <div class="mx-auto mt-s10 h-s24 w-s24">
      {@html flashLightIcon}
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
