<script>
  export let label = "";
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
  export let horizontalBottom = false;
  export let noPadding = false;
  export let flashSuccess = false;
  let px, py, iw, ih, ts, lead;
  if (small) {
    px = "px-5/4";
    py = "py-3/4";
    iw = "w-3";
    ih = "h-3";
    ts = "text-sm";
    lead = "leading-normal";
  } else if (big) {
    px = "px-5/2";
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
  if (noPadding) {
    px = "";
  }
  let border, text, background;
  if (secondary) {
    border =
      "border border-dora-magenta-cta hover:border-dora-magenta-hover disabled:border-gray-01 active:border-france-blue";
    text =
      "font-bold text-dora-magenta-cta hover:text-white disabled:disabled:text-gray-text-alt2 active:text-france-blue";
    background = "bg-white hover:bg-dora-magenta-hover";
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
        "font-bold text-dora-magenta-cta hover:text-dora-magenta-hover disabled:text-gray-text active:text-france-blue";
      background = "bg-transparent";
    } else {
      text = "font-bold text-white disabled:text-gray-text";
      background =
        "bg-dora-magenta-cta hover:bg-dora-magenta-hover disabled:bg-gray-01 active:bg-france-blue";
    }
  }
</script>

<style>
  .nogrow {
    align-self: flex-start;
  }

  .hz-bottom {
    align-self: flex-end;
    margin-bottom: 14px;
  }

  .flash-success {
    border: none;
    background-color: var(--col-success);
    color: var(--col-white);
  }

  .flash-success:hover {
    background-color: var(--col-success);
    color: var(--col-white);
  }

  .flash-success:focus {
    box-shadow: none;
  }
</style>

<button
  {type}
  {name}
  class="{px} {py} {ts} {lead} {border} {text} {background}  flex flex-row items-center justify-center text-center rounded focus:shadow-focus outline-none"
  class:nogrow
  class:hz-bottom={horizontalBottom}
  class:flash-success={flashSuccess}
  on:click
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
