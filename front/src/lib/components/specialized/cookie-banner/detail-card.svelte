<script lang="ts">
  import { slide } from "svelte/transition";
  import RadioButtons from "$lib/components/inputs/radio-buttons.svelte";
  import ArrowUpSLineArrows from "svelte-remix/ArrowUpSLineArrows.svelte";
  import ArrowDownSLineArrows from "svelte-remix/ArrowDownSLineArrows.svelte";
  import type { ConsentConfig } from "$lib/utils/consent.svelte";

  const TRANSITION_DURATION = 300;

  interface Props {
    categoryConfig: ConsentConfig;
    toggleConsentByKey: (consentKey: string) => void;
    disabled: boolean;
    value: boolean;
  }

  let {
    categoryConfig,
    toggleConsentByKey,
    disabled,
    value = $bindable(),
  }: Props = $props();

  let showCookieDetails = $state(false);
  let detailsContainer = $state<HTMLDivElement | undefined>();

  if (categoryConfig.consentKey === "required") {
    value = true;
  }

  $effect(() => {
    if (showCookieDetails && detailsContainer) {
      setTimeout(() => {
        detailsContainer?.scrollIntoView({ behavior: "smooth", block: "end" });
      }, TRANSITION_DURATION + 50);
    }
  });
</script>

{#snippet card(title = "", description = "", id = "", link = "")}
  <div>
    <div class="flex flex-col justify-between md:flex-row">
      <div class={["md:pr-s64 pr-0", { "ml-s8": link }]}>
        <h2 class={link ? "text-f16" : "text-f20"}>{title}</h2>
        <p class="text-f16">{description}</p>
      </div>
      <div class="mb-s8 md:mb-0">
        <RadioButtons
          {id}
          bind:group={value}
          choices={[
            {
              value: true,
              label: "Accepter",
            },
            {
              value: false,
              label: "Refuser",
            },
          ]}
          horizontal
          onchange={() => toggleConsentByKey(categoryConfig.consentKey)}
          {disabled}
        />
      </div>
    </div>
    {#if link}
      <a
        class="text-gray-text text-f16 ml-s8 underline"
        target="_blank"
        rel="noopener noreferrer"
        href={link}>Voir le site officiel</a
      >
    {/if}
  </div>
{/snippet}

<div
  class="gap-s64 border-color-gray pt-s8 border-b-gray-02 flex-col justify-between border-b-1"
>
  {@render card(
    categoryConfig.title,
    categoryConfig.description,
    categoryConfig.consentKey
  )}
  <div class="mb-s8 flex flex-col">
    {#if categoryConfig.consentKey !== "required"}
      {#if !showCookieDetails}
        <button
          class="text-magenta-cta flex underline"
          onclick={() => (showCookieDetails = !showCookieDetails)}
        >
          Voir plus de détails <ArrowDownSLineArrows />
        </button>
      {:else}
        <button
          class="text-magenta-cta mb-s8 flex underline"
          onclick={() => (showCookieDetails = !showCookieDetails)}
        >
          Cacher les détails <ArrowUpSLineArrows />
        </button>
        <div
          bind:this={detailsContainer}
          transition:slide={{ duration: TRANSITION_DURATION }}
        >
          {#each categoryConfig.cookies as cookie, i}
            {@render card(
              cookie.title,
              cookie.description,
              `${categoryConfig.consentKey}-cookie-${i}`,
              cookie.link
            )}
          {/each}
        </div>
      {/if}
    {/if}
  </div>
</div>
