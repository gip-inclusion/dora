<script lang="ts">
  import RadioButtons from "$lib/components/inputs/radio-buttons.svelte";
  import ArrowUpSLineArrows from "svelte-remix/ArrowUpSLineArrows.svelte";
  import ArrowDownSLineArrows from "svelte-remix/ArrowDownSLineArrows.svelte";
  import { MOBILE_BREAKPOINT } from "$lib/consts";

  let {
    categoryConfig,
    toggleConsentByKey,
    disabled = false,
    value = $bindable(),
  } = $props();

  let showCookieDetails = $state(false);
  let detailsContainer: HTMLDivElement | undefined = $state();

  if (categoryConfig.consentKey === "required") {
    value = true;
  }

  let innerWidth = $state(0);

  $effect(() => {
    if (showCookieDetails && detailsContainer) {
      setTimeout(() => {
        detailsContainer?.scrollIntoView({ behavior: "smooth", block: "end" });
      }, 100);
    }
  });
</script>

{#snippet card(title, description, id, link = null)}
  <div>
    <div class="flex justify-between">
      <div class="md:pr-s64 pr-s32 max-w-1/2 md:max-w-full">
        <h2 class="text-[1.25rem]">{title}</h2>
        <p class="text-[1rem]">{description}</p>
      </div>
      <div class="max-w-1/2 md:max-w-full">
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
          horizontal={innerWidth > MOBILE_BREAKPOINT}
          onchange={() => toggleConsentByKey(categoryConfig.consentKey)}
          {disabled}
        />
      </div>
    </div>
    {#if link}
      <a class="text-gray-text text-[1rem] underline" href={link}
        >Voir le site officiel</a
      >
    {/if}
  </div>
{/snippet}

<svelte:window bind:innerWidth />
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
        <div
          class="text-magenta-cta flex underline"
          on:click={() => (showCookieDetails = !showCookieDetails)}
        >
          Voir plus de détails <ArrowDownSLineArrows />
        </div>
      {:else}
        <div
          class="text-magenta-cta mb-s8 flex underline"
          on:click={() => (showCookieDetails = !showCookieDetails)}
        >
          Cacher les détails <ArrowUpSLineArrows />
        </div>
        <div bind:this={detailsContainer}>
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
