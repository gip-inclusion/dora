<script>
  import { arrowLeftIcon, arrowRightIcon } from "$lib/icons.js";
  import Button from "$lib/components/button.svelte";
</script>

<div class="flex flex-col items-start gap-3">
  <Button type="button" label="Bouton simple" />

  <Button type="button" label="Bouton simple" icon={arrowLeftIcon} iconOnLeft />

  <Button
    type="button"
    label="Bouton simple"
    icon={arrowRightIcon}
    iconOnRight />

  <Button type="button" icon={arrowRightIcon} />

  <Button
    type="button"
    label="Bouton desactivé"
    disabled
    icon={arrowLeftIcon}
    iconOnLeft />
</div>
