<script lang="ts">
  export let label = "";
  export let type: "button" | "submit" = "button";
  export let id: string | undefined = undefined;
  export let name: string | undefined = undefined;
  export let icon: string | undefined = undefined;
  export let extraClass = "";
  export let iconOnRight = false;
  export let hideLabel = false;
  export let disabled = false;
  export let small = false;
  export let secondary = false;
  export let noBackground = false;
  export let noPadding = false;
  export let hoverUnderline = false;
  export let wFull = false;
  export let preventDefaultOnMouseDown = false;
  export let ariaAttributes: Partial<{
    "aria-expanded": boolean;
    "aria-controls": string;
  }> = {};

  let paddingX: string, paddingY: string, textSize: string;

  if (small) {
    paddingY = "py-s6";
    textSize = "text-f14";
  } else {
    paddingY = "py-s12";
    textSize = "text-f16";
  }

  if (noPadding) {
    paddingX = "";
  } else if (small) {
    paddingX = label ? "px-s12" : "px-s8";
  } else {
    paddingX = "px-s20";
  }

  let border: string, text: string, background: string;

  $: {
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
  }
  const iconWidth = small ? "w-s24" : "w-s32";
  const iconHeight = small ? "h-s24" : "h-s32";

  function handleMouseDown(evt) {
    if (preventDefaultOnMouseDown) {
      evt.preventDefault();
    }
  }
</script>

<button
  {id}
  {type}
  {name}
  class="{paddingX} {paddingY} {textSize} {border} {text} {extraClass} {background}  break-words rounded leading-normal outline-none focus:shadow-focus"
  class:w-full={wFull}
  class:hover:underline={hoverUnderline}
  class:flex={icon}
  class:flex-row={icon}
  class:items-center={icon}
  {...ariaAttributes}
  on:click
  on:mousedown={handleMouseDown}
  {disabled}
>
  {#if icon && !iconOnRight}
    <span
      class="{iconWidth} {iconHeight} fill-current"
      class:mr-s8={!!label && !hideLabel}
      class:-my-s2={small}
    >
      {@html icon}
    </span>
  {/if}

  <span class:sr-only={hideLabel}>{label}</span>

  {#if iconOnRight}
    <span
      class="{iconWidth} {iconHeight} ml-s8 justify-end fill-current"
      class:-my-s2={small}
    >
      {@html icon}
    </span>
  {/if}
</button>
