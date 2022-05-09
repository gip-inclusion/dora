<script>
  export let selfStart = false;

  export let bgColorClass = "bg-magenta-20";
  export let textColorClass = "text-magenta-cta";
</script>

<span
  class="rounded px-s8 py-s2 text-f12 font-bold uppercase {textColorClass} {bgColorClass}"
  class:self-start={selfStart}
>
  <slot />
</span>
