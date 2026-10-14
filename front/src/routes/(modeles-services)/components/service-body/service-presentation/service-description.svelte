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

<ServiceSection title="Présentation">
  <div class="markdown-wrapper prose w-full">
    {#if service.description}
      <TextClamp
        text={markdownToHTML(service.description, 4)}
        clampedHeight={220}
      />
    {:else}
      <span>Description non renseignée</span>
    {/if}
  </div>
</ServiceSection>

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

  .prose,
  .markdown-wrapper :global(.prose) {
    max-width: 100%;
  }
</style>
