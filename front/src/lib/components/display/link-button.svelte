<script lang="ts">
  interface Props {
    to: string;
    otherTab?: boolean;
    nofollow?: boolean;
    label?: string;
    extraClass?: string;
    ariaLabel?: string;
    id?: string;
    icon?: string;
    iconOnRight?: boolean;
    small?: boolean;
    noBackground?: boolean;
    secondary?: boolean;
    hoverUnderline?: boolean;
    canWrap?: boolean;
    wFull?: boolean;
    onclick?: (event: MouseEvent) => void;
  }

  let {
    to,
    otherTab = false,
    nofollow = false,
    label = "",
    extraClass = "",
    ariaLabel,
    id,
    icon,
    iconOnRight = false,
    small = false,
    noBackground = false,
    secondary = false,
    hoverUnderline = false,
    canWrap = false,
    wFull = false,
    onclick,
  }: Props = $props();

  let paddingX: string = $state(),
    paddingY: string = $state(),
    textSize: string = $state();

  if (small) {
    paddingY = "py-s6";
    textSize = "text-f14";
  } else {
    paddingY = "py-s12";
    textSize = "text-f16";
  }

  if (small) {
    paddingX = label ? "px-s12" : "px-s8";
  } else {
    paddingX = "px-s20";
  }

  let border: string = $state(),
    text: string = $state(),
    background: string = $state();

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

  const iconWidth = "w-s24";
  const iconHeight = "h-s24";
</script>

<a
  {id}
  target={otherTab ? "_blank" : ""}
  title={otherTab ? "Ouverture dans une nouvelle fenêtre" : ""}
  rel="noopener {nofollow ? 'nofollow' : ''}"
  href={to}
  {onclick}
  class="{paddingX} {paddingY} {textSize} {border} {text} {background} {extraClass} focus:shadow-focus inline-flex items-center justify-center rounded-sm leading-normal whitespace-nowrap"
  class:w-full={wFull}
  class:hover:underline={hoverUnderline}
  aria-label={ariaLabel}
  class:whitespace-nowrap={!canWrap}
>
  {#if icon && !iconOnRight}
    <i
      class="{iconWidth} {iconHeight} shrink-0 fill-current"
      class:mr-s8={!!label}
      class:-my-s2={small}
    >
      {@html icon}
    </i>
  {/if}

  {label}

  {#if iconOnRight}
    <i
      class="{iconWidth} {iconHeight} ml-s8 shrink-0 fill-current"
      class:-my-s2={small}
    >
      {@html icon}
    </i>
  {/if}
</a>
