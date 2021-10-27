<script>
  import Button from "./button.svelte";

  export let to;
  export let otherTab = false;
  export let nofollow = false;
  export let small = false;
  export let noPadding = false;
  export let ariaLabel = undefined;
</script>

<a
  target={otherTab ? "_blank" : "_self"}
  rel="noopener {nofollow ? 'nofollow' : ''}"
  href={to}
>
  <Button type="button" {...$$restProps} {ariaLabel} {small} {noPadding} />
</a>
