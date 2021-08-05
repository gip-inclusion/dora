<script>
  import { coperCoinFillIcon } from "$lib/icons.js";
  import Button from "$lib/components/button.svelte";

  export let noBackground = false;
  export let label;
  export let big = false,
    small = false;
  export let secondary = false,
    tertiary = false;
</script>

<Button
  type="button"
  {label}
  {big}
  {small}
  {secondary}
  {tertiary}
  {noBackground} />
<Button
  type="button"
  {label}
  {big}
  {small}
  {secondary}
  {tertiary}
  {noBackground}
  icon={coperCoinFillIcon}
  iconOnLeft />
<Button
  type="button"
  {label}
  {big}
  {small}
  {secondary}
  {tertiary}
  {noBackground}
  icon={coperCoinFillIcon}
  iconOnRight />
<Button
  type="button"
  {big}
  {small}
  {secondary}
  {tertiary}
  {noBackground}
  icon={coperCoinFillIcon} />
<Button
  type="button"
  {big}
  {small}
  {secondary}
  {tertiary}
  {noBackground}
  {label}
  disabled
  icon={coperCoinFillIcon}
  iconOnLeft />
