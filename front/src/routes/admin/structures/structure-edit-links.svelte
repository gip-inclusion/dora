<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";

  interface Props {
    structureSlug: string;
    small?: boolean;
  }

  let { structureSlug, small = false }: Props = $props();
</script>

<div class="gap-s16 flex flex-row flex-wrap justify-end">
  <LinkButton
    label="Modifier les services"
    to="/structures/{structureSlug}/services"
    otherTab
    secondary
    {small}
  />
  <LinkButton
    label="Modifier la structure"
    to="/structures/{structureSlug}"
    otherTab
    secondary
    {small}
  />
  <LinkButton
    label="Gérer les administrateurs"
    to="/structures/{structureSlug}/collaborateurs"
    otherTab
    {small}
  />
</div>
