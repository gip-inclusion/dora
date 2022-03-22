<script>
  export let to;
  export let otherTab = false;
  export let nofollow = false;

  export let label = "";
  export let ariaLabel = undefined;
  export let icon = null;
  export let iconOnRight = false;
  export let small = false;
  export let noBackground = false;
  export let noPadding = false;
  export let secondary = false;

  export let wFull = false;

  let px, py, ts;

  if (small) {
    py = "py-s6";
    ts = "text-f14";
  } else {
    py = "py-s12";
    ts = "text-f16";
  }

  if (noPadding) {
    px = "";
  } else if (small) {
    px = "px-s16";
  } else {
    px = "px-s20";
  }

  let border, text, background;

  border = "border-0";

  if (secondary) {
    border =
      "border border-magenta-cta hover:border-magenta-hover disabled:border-gray-01 active:border-france-blue";
    text =
      "font-bold text-magenta-cta hover:text-white disabled:text-gray-text-alt2 active:text-france-blue";
    background = "bg-white hover:bg-magenta-hover disabled:bg-white";
  } else {
    border = "border-0";

    if (noBackground) {
      text =
        "font-bold text-magenta-cta hover:text-magenta-hover disabled:text-gray-text active:text-france-blue";
      background = "bg-transparent";
    } else {
      text = "font-bold text-white disabled:text-gray-text";
      background =
        "bg-magenta-cta hover:bg-magenta-hover disabled:bg-gray-01 active:bg-france-blue";
    }
  }

  const iw = "w-s24";
  const ih = "h-s24";
</script>

<a
  target={otherTab ? "_blank" : ""}
  rel="noopener {nofollow ? 'nofollow' : ''}"
  href={to}
  class="{px} {py} {ts} {border} {text} {background} inline-flex items-center justify-center whitespace-nowrap rounded leading-normal outline-none focus:shadow-focus"
  class:w-full={wFull}
  aria-label={ariaLabel}
>
  {#if icon && !iconOnRight}
    <div class="{iw} {ih} shrink-0 fill-current" class:mr-s8={!!label}>
      {@html icon}
    </div>
  {/if}

  {label}

  {#if iconOnRight}
    <div class="{iw} {ih} ml-s8 shrink-0 fill-current">
      {@html icon}
    </div>
  {/if}
</a>
