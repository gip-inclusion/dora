<script lang="ts">
  import TextClamp from "$lib/components/display/text-clamp.svelte";
  import type { Service } from "$lib/types";
  import { markdownToHTML } from "$lib/utils/misc";

  import ServiceSection from "./components/service-section.svelte";

  interface Props {
    service: Service;
  }

  let { service }: Props = $props();
</script>

{#if service.fullDesc}
  <ServiceSection title="Description du service">
    <div class="markdown-wrapper prose w-full">
      <TextClamp text={markdownToHTML(service.fullDesc, 4)} />
    </div>
  </ServiceSection>
{/if}

<style lang="postcss">
  @reference "../../../../../app.css";

  .markdown-wrapper :global(h1),
  .markdown-wrapper :global(h2),
  .markdown-wrapper :global(h3) {
    color: var(--col-gray-dark);
  }

  .markdown-wrapper :global(p),
  .markdown-wrapper :global(strong),
  .markdown-wrapper :global(li) {
    color: var(--col-text);
    font-size: 16px !important;
    line-height: 24px !important;
  }

  .prose {
    max-width: 100%;
  }
</style>
