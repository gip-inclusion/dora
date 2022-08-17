<script lang="ts">
  export let to: string;
  export let otherTab = false;
  export let nofollow = false;

  export let label = "";
  export let extraClass = "";
  export let ariaLabel: string | undefined = undefined;
  export let id: string | undefined = undefined;
  export let icon: string | undefined = undefined;
  export let iconOnRight = false;
  export let small = false;
  export let noBackground = false;
  export let secondary = false;

  export let wFull = false;

  let px: string, py: string, ts: string;

  if (small) {
    py = "py-s6";
    ts = "text-f14";
  } else {
    py = "py-s12";
    ts = "text-f16";
  }

  if (small) {
    px = label ? "px-s12" : "px-s8";
  } else {
    px = "px-s20";
  }

  let border: string, text: string, background: string;

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
  {id}
  target={otherTab ? "_blank" : ""}
  title={otherTab ? "Ouverture dans une nouvelle fenêtre" : ""}
  rel="noopener {nofollow ? 'nofollow' : ''}"
  href={to}
  on:click
  class="{px} {py} {ts} {border} {text} {background} {extraClass} inline-flex items-center justify-center whitespace-nowrap rounded leading-normal outline-none focus:shadow-focus"
  class:w-full={wFull}
  aria-label={ariaLabel}
>
  {#if icon && !iconOnRight}
    <i
      class="{iw} {ih} shrink-0 fill-current"
      class:mr-s8={!!label}
      class:-my-s2={small}
    >
      {@html icon}
    </i>
  {/if}

  {label}

  {#if iconOnRight}
    <i class="{iw} {ih} ml-s8 shrink-0 fill-current" class:-my-s2={small}>
      {@html icon}
    </i>
  {/if}
</a>
