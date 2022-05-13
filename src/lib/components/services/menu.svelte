<script>
  import LinkButton from "$lib/components/link-button.svelte";

  export let service;
  export let secondary = false;
</script>

<div>
  <LinkButton
    label="Modifier"
    to="/services/{service.slug}/editer"
    small
    noBackground={!secondary}
    {secondary}
  />
</div>
