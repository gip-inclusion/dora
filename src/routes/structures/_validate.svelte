<script>
  import Button from "$lib/components/button.svelte";
  import { arrowRightSIcon } from "$lib/icons.js";

  export let disabled = false;
</script>

<Button
  {disabled}
  on:submit
  name="validate"
  type="submit"
  label="Validez les informations"
  icon={arrowRightSIcon}
  iconOnRight
  preventDefaultOnMouseDown
/>
