<script lang="ts">
  /* eslint-disable svelte/no-at-html-tags */
  /*
   * Pour des raisons de sécurité, on centralise l'affichage du rendu Markdown
   * en utilisant @html dans ce fichier.
   * On utilise markdownToHTML() qui nettoie le HTML avec sanitize-html.
   */
  import { markdownToHTML } from "#lib/utils/markdown.ts";

  interface Props {
    content: string;
    titleLevel?: number;
  }

  let { content, titleLevel }: Props = $props();

  const html = $derived(markdownToHTML(content, titleLevel));
</script>

{@html html}
