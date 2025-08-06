<script lang="ts">
  /* eslint-disable svelte/no-at-html-tags */
  /*
   * Pour des raisons de sécurité, on centralise l'affichage du rendu Markdown
   * en utilisant @html dans ce fichier.
   * On utilise markdownToHTML() qui fait appel à insane() pour sécuriser le HTML.
   */
  import { markdownToHTML } from "$lib/utils/misc";

  interface Props {
    content: string;
    titleLevel?: number;
  }

  let { content, titleLevel }: Props = $props();

  const html = markdownToHTML(content, titleLevel);
</script>

{@html html}
