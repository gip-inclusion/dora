<script>
  export let label = "";
  export let type = "button";
  export let name = null;
  export let icon = null;
  export let iconOnRight = false;
  export let disabled = false;
  export let small = false;
  export let secondary = false;
  export let noBackground = false;
  export let noPadding = false;
  export let flashSuccess = false;
  export let wFull = false;
  export let preventDefaultOnMouseDown = false;

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

  function handleMouseDown(evt) {
    if (preventDefaultOnMouseDown) evt.preventDefault();
  }
</script>

<button
  {type}
  {name}
  class="{px} {py} {ts} {border} {text} {background} whitespace-nowrap rounded leading-normal outline-none focus:shadow-focus"
  class:flash-success={flashSuccess}
  class:w-full={wFull}
  class:flex={icon}
  class:flex-row={icon}
  class:items-center={icon}
  on:click
  on:mousedown={handleMouseDown}
  {disabled}
>
  {#if icon && !iconOnRight}
    <span class="{iw} {ih} fill-current" class:mr-s8={!!label}>
      {@html icon}
    </span>
  {/if}

  {label}

  {#if iconOnRight}
    <span class="{iw} {ih} ml-s8 justify-end fill-current">
      {@html icon}
    </span>
  {/if}
</button>
