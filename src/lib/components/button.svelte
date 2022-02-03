<script>
  export let label = "";
  export let ariaLabel = undefined;
  export let type = "button";
  export let name = null;
  export let icon = null;
  export let iconOnLeft = false,
    iconOnRight = false;
  export let disabled = false;
  export let small = false,
    big = false;
  export let secondary = false,
    tertiary = false;
  export let noBackground = false;
  export let nogrow = false;
  export let noPadding = false;
  export let flashSuccess = false;
  export let wFull = false;

  // This will call preventDefault() on a mouseDown event
  // which will prevent the blur event on other nodes
  // which was changing the validation messages, which moved the
  // button, and broke the click event
  export let preventDefaultOnMouseDown = false;
  let px, py, iw, ih, ts, lead;
  if (small) {
    px = "px-s8 lg:px-s10";
    py = "py-s6";
    iw = "w-s24";
    ih = "h-s24";
    ts = "text-f14";
    lead = "leading-normal";
  } else if (big) {
    px = "px-s8 lg:px-s20";
    py = "py-s16";
    iw = "w-s32";
    ih = "h-s32";
    ts = "text-f16";
    lead = "leading-normal";
  } else {
    px = "px-s8 lg:px-s20";
    py = "py-s12";
    iw = "w-s24";
    ih = "h-s24";
    ts = "text-f16";
    lead = "leading-normal";
  }
  if (noPadding) {
    px = "";
  }
  let border, text, background;
  if (secondary) {
    border =
      "border border-magenta-cta hover:border-magenta-hover disabled:border-gray-01 active:border-france-blue";
    text =
      "font-bold text-magenta-cta hover:text-white disabled:text-gray-text-alt2 active:text-france-blue";
    background = "bg-white hover:bg-magenta-hover disabled:bg-white";
  } else if (tertiary) {
    border =
      "border border-gray-dark  disabled:border-gray-01 active:border-france-blue";
    text =
      "text-gray-text hover:text-white disabled:text-gray-text-alt2 active:text-france-blue";
    background = "bg-white hover:bg-gray-dark";
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

  function handleMouseDown(evt) {
    if (preventDefaultOnMouseDown) evt.preventDefault();
  }
</script>

<button
  {type}
  {name}
  class="{px} {py} {ts} {lead} {border} {text} {background} flex flex-row items-center whitespace-nowrap rounded outline-none focus:shadow-focus"
  class:items-start={nogrow}
  class:flash-success={flashSuccess}
  class:w-full={wFull}
  class:justify-center={!iconOnLeft && !iconOnRight}
  on:click
  on:mousedown={handleMouseDown}
  aria-label={ariaLabel}
  {disabled}
>
  {#if iconOnLeft}
    <div class="{iw} {ih} mr-s8 shrink-0 fill-current">
      {@html icon}
    </div>
  {/if}
  {#if icon && !label}
    <div class="{iw} {ih} fill-current">
      {@html icon}
    </div>
  {/if}
  {label}

  {#if iconOnRight}
    <div class="{iw} {ih} ml-s8 shrink-0 justify-end fill-current">
      {@html icon}
    </div>
  {/if}
</button>
