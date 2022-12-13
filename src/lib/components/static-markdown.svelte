<script lang="ts">
  import { markdownToHTML } from "$lib/utils";
  export let content;
</script>

<div class="prose max-w-3xl">
  {@html markdownToHTML(content, 1)}
</div>
