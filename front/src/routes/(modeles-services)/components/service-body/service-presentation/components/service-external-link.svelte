<script lang="ts">
  import ExternalLinkIcon from "$lib/components/display/external-link-icon.svelte";

  interface Props {
    href: string;
    label: string;
    /** Affiche l'icône « lien externe » à la suite du libellé */
    withIcon?: boolean;
  }

  let { href, label, withIcon = false }: Props = $props();
</script>

<a
  class="underline"
  target="_blank"
  {href}
  title="Ouverture dans une nouvelle fenêtre"
  rel="noopener noreferrer ugc"
  >{label}{#if withIcon}<ExternalLinkIcon />{/if}</a
>
