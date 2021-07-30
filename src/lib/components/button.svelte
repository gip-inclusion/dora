<script>
  export let label = "";
  export let icon;
  export let iconOnLeft;
  export let iconOnRight;
  export let type = "button";
  export let disabled;
  export let small;
  export let big;

  let px, py, iw, ih, ts, lead;
  if (small) {
    px = "px-5/4";
    py = "py-3/4";
    iw = "w-3";
    ih = "h-3";
    ts = "text-sm";
    lead = "leading-normal";
  } else if (big) {
    px = "px-3";
    py = "py-2";
    iw = "w-4";
    ih = "h-4";
    ts = "text-base";
    lead = "leading-normal";
  } else {
    px = "px-5/2";
    py = "py-3/2";
    iw = "w-3";
    ih = "h-3";
    ts = "text-base";
    lead = "leading-normal";
  }
</script>

<button
  {type}
  class="{px} {py} {ts} {lead} flex flex-row items-center justify-center text-center text-white rounded bg-dora-magenta-cta hover:bg-dora-magenta-hover disabled:bg-gray-01 disabled:text-gray-text active:bg-france-blue focus:shadow-focus outline-none "
  {disabled}>
  {#if iconOnLeft}
    <div class="{iw} {ih} mr-1 fill-current ">
      {@html icon}
    </div>
  {/if}
  {#if icon && !label}
    <div class="{iw} {ih} fill-current ">
      {@html icon}
    </div>
  {/if}
  {label}
  {#if iconOnRight}
    <div class="{iw} {ih} ml-1 fill-current">
      {@html icon}
    </div>
  {/if}
</button>
