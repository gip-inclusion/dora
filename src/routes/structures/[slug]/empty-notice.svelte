<script lang="ts">
  import { externalLinkIcon } from "$lib/icons";

  export let textTopIcon = "";
  export let title = "";
  export let illustration = "";
  export let links: { label: string; url: string }[] = [];
</script>

<div class="flex flex-col rounded-md border border-gray-03 p-s40 md:flex-row">
  <div class="flex flex-[4] flex-col">
    <div class="mb-s14 text-center">
      <span
        class="ml-s10 inline-block h-s24 w-s24 fill-current text-gray-text-alt2"
      >
        {@html textTopIcon}
      </span>
    </div>
    <h3 class="text-center text-f30 leading-40 text-gray-text">{title}</h3>

    <div class="text-gray-text">
      <slot />

      <div class="mt-s20 text-center">
        <ul class="flex flex-col gap-s20 text-magenta-cta">
          {#each links as { label, url }}
            <li class="flex justify-center">
              <a
                href={url}
                class="flex items-center"
                title="Ouverture dans une nouvelle fenêtre"
                target="_blank"
                rel="noopener noreferrer"
              >
                {label}
                <span class="ml-s8 block h-s20 w-s20 fill-current" aria-hidden>
                  {@html externalLinkIcon}
                </span>
              </a>
            </li>
          {/each}
        </ul>
      </div>
    </div>
  </div>

  <div class="flex flex-[3] items-center justify-center">
    <img alt="" src={illustration} />
  </div>
</div>
