<script lang="ts">
  export let selfStart = false;

  export let bgColorClass = "bg-gray-text-alt";
  export let textColorClass = "text-white";
</script>

<span
  class="break-word rounded px-s8 py-s2 text-f14 font-bold {textColorClass} {bgColorClass}"
  class:self-start={selfStart}
>
  <slot />
</span>
