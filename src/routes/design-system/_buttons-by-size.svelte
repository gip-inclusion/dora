<script>
  import { coperCoinFillIcon } from "$lib/icons.js";
  import Button from "$lib/components/button.svelte";

  export let label;
  export let big, small;
  export let secondary, tertiary;
</script>

<Button type="button" {label} {big} {small} {secondary} {tertiary} />
<Button
  type="button"
  {label}
  {big}
  {small}
  {secondary}
  {tertiary}
  icon={coperCoinFillIcon}
  iconOnLeft />
<Button
  type="button"
  {label}
  {big}
  {small}
  {secondary}
  {tertiary}
  icon={coperCoinFillIcon}
  iconOnRight />
<Button
  type="button"
  {big}
  {small}
  {secondary}
  {tertiary}
  icon={coperCoinFillIcon} />
<Button
  type="button"
  {big}
  {small}
  {secondary}
  {tertiary}
  {label}
  disabled
  icon={coperCoinFillIcon}
  iconOnLeft />
