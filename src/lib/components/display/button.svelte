<script lang="ts">
  export let label = "";
  export let type: "button" | "submit" = "button";
  export let id: string | undefined = undefined;
  export let name: string | undefined = undefined;
  export let icon: string | undefined = undefined;
  export let extraClass = "";
  export let iconOnRight = false;
  export let disabled = false;
  export let small = false;
  export let secondary = false;
  export let noBackground = false;
  export let noPadding = false;
  export let hoverUnderline = false;
  export let wFull = false;
  export let preventDefaultOnMouseDown = false;

  let px: string, py: string, ts: string;

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
    px = label ? "px-s12" : "px-s8";
  } else {
    px = "px-s20";
  }

  let border: string, text: string, background: string;

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

  const iw = small ? "w-s24" : "w-s32";
  const ih = small ? "h-s24" : "h-s32";

  function handleMouseDown(evt) {
    if (preventDefaultOnMouseDown) evt.preventDefault();
  }
</script>

<button
  {id}
  {type}
  {name}
  class="{px} {py} {ts} {border} {text} {extraClass} {background} whitespace-nowrap rounded leading-normal outline-none focus:shadow-focus"
  class:w-full={wFull}
  class:hover:underline={hoverUnderline}
  class:flex={icon}
  class:flex-row={icon}
  class:items-center={icon}
  on:click
  on:mousedown={handleMouseDown}
  {disabled}
>
  {#if icon && !iconOnRight}
    <span
      class="{iw} {ih} fill-current"
      class:mr-s8={!!label}
      class:-my-s2={small}
    >
      {@html icon}
    </span>
  {/if}

  {label}

  {#if iconOnRight}
    <span class="{iw} {ih} ml-s8 justify-end fill-current" class:-my-s2={small}>
      {@html icon}
    </span>
  {/if}
</button>
