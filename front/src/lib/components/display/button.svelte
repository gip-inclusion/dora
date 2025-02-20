<script lang="ts">
  import { run, createBubbler } from 'svelte/legacy';

  const bubble = createBubbler();
  interface Props {
    label?: string;
    type?: "button" | "submit";
    id?: string | undefined;
    name?: string | undefined;
    icon?: string | undefined;
    title?: string | undefined;
    extraClass?: string;
    iconOnRight?: boolean;
    hideLabel?: boolean;
    disabled?: boolean;
    small?: boolean;
    big?: boolean;
    secondary?: boolean;
    noBackground?: boolean;
    noPadding?: boolean;
    hoverUnderline?: boolean;
    wFull?: boolean;
    noWrap?: boolean;
    preventDefaultOnMouseDown?: boolean;
    ariaAttributes?: Partial<{
    "aria-expanded": boolean;
    "aria-controls": string;
  }>;
  }

  let {
    label = "",
    type = "button",
    id = undefined,
    name = undefined,
    icon = undefined,
    title = undefined,
    extraClass = "",
    iconOnRight = false,
    hideLabel = false,
    disabled = false,
    small = false,
    big = false,
    secondary = false,
    noBackground = false,
    noPadding = false,
    hoverUnderline = false,
    wFull = false,
    noWrap = false,
    preventDefaultOnMouseDown = false,
    ariaAttributes = {}
  }: Props = $props();

  let paddingX: string = $state(), paddingY: string = $state(), textSize: string = $state();

  if (small) {
    paddingY = "py-s6";
    textSize = "text-f14";
  } else if (big) {
    paddingY = "py-s12";
    textSize = "text-f23";
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

  let border: string = $state(), text: string = $state(), background: string = $state();

  run(() => {
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
  });
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
  {title}
  class="{paddingX} {paddingY} {textSize} {border} {text} {extraClass} {background}  focus:shadow-focus rounded-sm leading-normal break-words outline-hidden"
  class:w-full={wFull}
  class:whitespace-nowrap={noWrap}
  class:hover:underline={hoverUnderline}
  class:flex={icon}
  class:flex-row={icon}
  class:items-center={icon}
  {...ariaAttributes}
  onclick={bubble('click')}
  onmousedown={handleMouseDown}
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
