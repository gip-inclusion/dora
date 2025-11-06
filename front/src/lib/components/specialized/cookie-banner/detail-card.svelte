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

  if (categoryConfig.consentKey === "required") {
    value = true;
  }
</script>

{#snippet card(title, description, id)}
  <div>
    <div class="flex justify-between">
      <div>
        <h2 class="text-[1.25rem]">{title}</h2>
        <p class="text-[1rem]">{description}</p>
      </div>
      <div>
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
  </div>
{/snippet}

<div
  class="gap-s64 border-color-gray pt-s8 flex-col justify-between border-b-1"
>
  {@render card(
    categoryConfig.title,
    categoryConfig.description,
    categoryConfig.consentKey
  )}
  <div class="flex flex-col">
    {#if !showCookieDetails}
      <div
        class="flex"
        on:click={() => (showCookieDetails = !showCookieDetails)}
      >
        Voir plus de détails <ArrowDownSLineArrows />
      </div>
    {:else}
      <div
        class="flex"
        on:click={() => (showCookieDetails = !showCookieDetails)}
      >
        Cacher les détails <ArrowUpSLineArrows />
      </div>
      {#each categoryConfig.cookies as cookie, i}
        {@render card(
          cookie.title,
          cookie.description,
          `${categoryConfig.consentKey}-cookie-${i}`
        )}
      {/each}
    {/if}
  </div>
</div>
