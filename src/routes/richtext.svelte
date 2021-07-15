<script>
  import Tiptap from "$lib/tiptap.svelte";
  import { htmlToMarkdown } from "$lib/utils";
  let content = "";
</script>

<div class="w-3/4 m-5 mx-auto">
  <Tiptap
    bind:htmlContent={content}
    className="prose prose-sm p-2 w-full max-w-none h-64 border-2 overflow-auto focus:outline-none" />

  <pre
    class="w-full h-64 p-2 mt-8 overflow-auto font-mono bg-gray-200">
    {htmlToMarkdown(content)}
  </pre>
</div>
