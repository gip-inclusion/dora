<script>
  import LinkButton from "$lib/components/link-button.svelte";
</script>

<div class="flex row-start-1">
  <div class="mx-auto grid grid-cols-main gap-x-3 gap-y-3">
    <div class="col-start-1 col-span-full">
      <LinkButton label="Design System" to="design-system" noBackground />
      <LinkButton
        label="Création de structure"
        to="/structures/creer"
        noBackground />
      <LinkButton
        label="Création de service"
        to="/services/creer"
        noBackground />
    </div>
  </div>
</div>
