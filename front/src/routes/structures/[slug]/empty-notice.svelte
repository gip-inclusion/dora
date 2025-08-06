<script lang="ts">
  import type { Component, Snippet } from "svelte";

  import ExternalLinkLineSystem from "svelte-remix/ExternalLinkLineSystem.svelte";

  interface Props {
    textTopIcon: Component;
    title?: string;
    illustration?: string;
    links?: { label: string; url: string }[];
    children?: Snippet;
  }

  let {
    textTopIcon: TextTopIcon,
    title = "",
    illustration = "",
    links = [],
    children,
  }: Props = $props();
</script>

<div class="border-gray-03 p-s40 flex flex-col rounded-lg border md:flex-row">
  <div class="flex flex-4 flex-col">
    <div class="mb-s14 text-center">
      <span
        class="ml-s10 h-s24 w-s24 text-gray-text-alt2 inline-block fill-current"
      >
        <TextTopIcon />
      </span>
    </div>
    <h3 class="text-f30 text-gray-text text-center leading-40">{title}</h3>

    <div class="text-gray-text">
      {@render children?.()}

      <div class="mt-s20 text-center">
        <ul class="gap-s20 text-magenta-cta flex flex-col">
          {#each links as { label, url }}
            <li class="flex justify-center">
              <a
                href={url}
                title="Ouverture dans une nouvelle fenêtre"
                target="_blank"
                rel="noopener"
              >
                {label}
                <span
                  class="h-s20 w-s20 pt-s4 inline-block fill-current"
                  aria-hidden="true"
                >
                  <ExternalLinkLineSystem size="20" />
                </span>
              </a>
            </li>
          {/each}
        </ul>
      </div>
    </div>
  </div>

  <div class="flex flex-3 items-center justify-center">
    <img alt="" src={illustration} />
  </div>
</div>
