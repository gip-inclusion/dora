<script>
  export let selfStart = false;

  export let bgColorClass = "bg-magenta-20";
  export let fgColorClass = "text-magenta-cta";
</script>

<div
  class="px-s8 py-s2 rounded {fgColorClass} text-f12 font-bold uppercase {bgColorClass}"
  class:self-start={selfStart}
>
  <slot />
</div>
