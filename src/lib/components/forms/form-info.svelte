<script lang="ts">
  import { informationIcon } from "$lib/icons";
  export let title;
  export let icon;
</script>

<div class="my-s32 rounded-md bg-info-light p-s16">
  {#if title}
    <div class="mb-s8 flex items-center text-f17 font-bold text-info">
      <div class="mr-s8 h-s24 w-s24 fill-current">
        {@html icon || informationIcon}
      </div>
      {title}
    </div>
  {/if}
  <div class="text-f14 leading-24 text-gray-text">
    <slot />
  </div>
</div>
