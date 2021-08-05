<script>
  import LinkButton from "$lib/components/link-button.svelte";
</script>

<div
  class="flex flex-col items-start col-start-1 row-start-1 gap-3 col-span-full">
  <LinkButton label="Design System" to="design-system" noBackground />
  <LinkButton
    label="Création de structure"
    to="/structures/creer"
    noBackground />
  <LinkButton label="Création de service" to="/services/creer" noBackground />
</div>
