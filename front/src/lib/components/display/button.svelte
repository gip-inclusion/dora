<script lang="ts">
  import type { Component } from "svelte";
  import Spinner from "./spinner.svelte";

  interface Props {
    label?: string;
    type?: "button" | "submit";
    id?: string;
    name?: string;
    icon?: Component;
    title?: string;
    extraClass?: string;
    iconOnRight?: boolean;
    hideLabel?: boolean;
    disabled?: boolean;
    loading?: boolean;
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
    onclick?: (event: MouseEvent) => void;
  }

  let {
    label = "",
    type = "button",
    id,
    name,
    icon: Icon,
    title,
    extraClass = "",
    iconOnRight = false,
    hideLabel = false,
    disabled = false,
    loading = false,
    small = false,
    big = false,
    secondary = false,
    noBackground = false,
    noPadding = false,
    hoverUnderline = false,
    wFull = false,
    noWrap = false,
    preventDefaultOnMouseDown = false,
    ariaAttributes = {},
    onclick,
  }: Props = $props();

  let paddingX: string = $derived.by(() => {
    if (noPadding) {
      return "";
    }
    if (small) {
      return label ? "px-s12" : "px-s8";
    }
    return "px-s20";
  });
  let paddingY: string = $derived.by(() => {
    if (small) {
      return "py-s6";
    }
    if (big) {
      return "py-s12";
    }
    return "py-s12";
  });
  let textSize: string = $derived.by(() => {
    if (small) {
      return "text-f14";
    }
    if (big) {
      return "text-f23";
    }
    return "text-f16";
  });
  let border: string = $derived.by(() => {
    if (secondary) {
      return "border border-magenta-cta hover:border-magenta-hover disabled:border-gray-01 active:border-france-blue";
    }
    return "border-0";
  });
  let text: string = $derived.by(() => {
    if (secondary) {
      return "font-bold text-magenta-cta hover:text-white disabled:text-gray-text-alt2 active:text-france-blue";
    }
    if (noBackground) {
      return "font-bold text-magenta-cta hover:text-magenta-hover disabled:text-gray-text active:text-france-blue";
    }
    return "font-bold text-white disabled:text-gray-text";
  });
  let background: string = $derived.by(() => {
    if (secondary) {
      return "bg-white hover:bg-magenta-hover disabled:bg-white";
    }
    if (noBackground) {
      return "bg-transparent";
    }
    return "bg-magenta-cta hover:bg-magenta-hover disabled:bg-gray-01 active:bg-france-blue";
  });

  const iconWidth = "w-s24";
  const iconHeight = "h-s24";

  function handleMouseDown(evt: MouseEvent) {
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
  class:flex={!!Icon || loading}
  class:flex-row={!!Icon || loading}
  class:items-center={!!Icon || loading}
  {...ariaAttributes}
  {onclick}
  onmousedown={handleMouseDown}
  disabled={disabled || loading}
>
  {#if loading}
    <span
      class="{iconWidth} {iconHeight}"
      class:mr-s8={!!label && !hideLabel}
      class:-my-s2={small}
    >
      <Spinner size="100%" colorClass="border-gray-text" />
    </span>
  {:else if Icon && !iconOnRight}
    <span
      class="{iconWidth} {iconHeight} fill-current"
      class:mr-s8={!!label && !hideLabel}
      class:-my-s2={small}
    >
      <Icon />
    </span>
  {/if}

  <span class:sr-only={hideLabel}>{label}</span>

  {#if Icon && iconOnRight && !loading}
    <span
      class="{iconWidth} {iconHeight} ml-s8 justify-end fill-current"
      class:-my-s2={small}
    >
      <Icon />
    </span>
  {/if}
</button>
