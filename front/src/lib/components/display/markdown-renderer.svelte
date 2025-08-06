<script lang="ts">
  import { markdownToHTML } from "$lib/utils/misc";

  interface Props {
    content: string;
    titleLevel?: number;
  }

  let { content, titleLevel }: Props = $props();

  const html = markdownToHTML(content, titleLevel);
</script>

{@html html}
