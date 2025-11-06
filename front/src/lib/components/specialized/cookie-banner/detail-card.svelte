<script lang="ts">
  import RadioButtons from "$lib/components/inputs/radio-buttons.svelte";
  import ArrowUpSLineArrows from "svelte-remix/ArrowUpSLineArrows.svelte";
  import ArrowDownSLineArrows from "svelte-remix/ArrowDownSLineArrows.svelte";

  let {
    categoryConfig,
    toggleConsentByKey,
    disabled = false,
    value = $bindable(),
  } = $props();

  let showCookieDetails = $state(false);
</script>

{#snippet card(title, description)}
  <div>
    <div class="flex">
      <div>
        <h2 class="text-[1.25rem]">{title}</h2>
        <p class="text-[1rem]">{description}</p>
      </div>
      <div>
        <RadioButtons
          id={categoryConfig.consentKey}
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
  </div>
{/snippet}

<div
  class="gap-s64 border-color-gray pt-s8 flex-col justify-between border-b-1"
>
  {@render card(categoryConfig.title, categoryConfig.description)}
  <div
    class="flex flex-col"
    on:click={() => (showCookieDetails = !showCookieDetails)}
  >
    {#if !showCookieDetails}
      <div class="flex">Voir plus de détails <ArrowDownSLineArrows /></div>
    {:else}
      <div class="flex">Cacher les détails <ArrowUpSLineArrows /></div>
      {#each categoryConfig.cookies as cookie}
        {@render card(cookie.title, cookie.description)}
      {/each}
    {/if}
  </div>
</div>
