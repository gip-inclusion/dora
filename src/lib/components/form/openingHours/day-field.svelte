<script lang="ts">
  import { alertIcon } from "$lib/icons";
  import type { Day, DayPeriod } from "$lib/types";
  import { createEventDispatcher } from "svelte";

  import ToggleCheckboxInput from "../toggle-checkbox-input.svelte";

  export let label: string;
  export let isOpen: boolean;
  export let touched: boolean;
  export let openAt: string;
  export let closeAt: string;
  export let day: Day;
  export let dayPeriod: DayPeriod;

  const dispatch = createEventDispatcher();

  let inError = false;
  let ariaDescribedBy = undefined;

  $: {
    if (isOpen && touched) {
      inError = !closeAt || !openAt;
      if (inError) {
        ariaDescribedBy = `error-${day}—${dayPeriod}`;
      }
    } else {
      inError = false;
    }
  }

  function handleUpdate() {
    // Clear values and notify change
    if (!isOpen) {
      openAt = "";
      closeAt = "";
      touched = false;
    }
    dispatch("change");
  }
</script>

<div class:disabled-bg={!isOpen}>
  <div
    class="flex w-full justify-around rounded-tl rounded-tr border border-gray-03 text-center text-gray-text"
    class:error={inError}
  >
    <span class="flex-1 border-r border-gray-03 py-s10 text-f18">
      {#if !isOpen}
        <span class="text-f19 text-gray-text-alt">/</span>
      {:else}
        <label class:error={inError}>
          <span class="sr-only">Horaire d'ouverture pour le {label}</span>
          <input
            on:change
            bind:value={openAt}
            type="time"
            aria-describedby={ariaDescribedBy}
          />
        </label>
      {/if}
    </span>

    <span class="flex-1 border-gray-03 py-s10 text-f18">
      {#if !isOpen}
        <span class="text-f19 text-gray-text-alt">/</span>
      {:else}
        <label class="flex-1 py-s10 ">
          <span class="sr-only">Horaire de fermeture pour le {label}</span>

          <input
            on:change
            bind:value={closeAt}
            disabled={!isOpen}
            class:disabled-bg={!isOpen}
            type="time"
          />
        </label>
      {/if}
    </span>
  </div>

  <div
    class="rounded-bl rounded-br border-r border-l border-b border-gray-03 py-s10 text-center text-gray-text"
    class:error={inError}
  >
    <label class="flex justify-center">
      <span class="sr-only">
        Ouvert {dayPeriod === "morning" ? "le matin" : "l'après-midi"}
      </span>

      <ToggleCheckboxInput
        on:change={handleUpdate}
        bind:checked={isOpen}
        yesLabel="Ouvert"
        noLabel="Fermé"
        name="{day}-{dayPeriod}-is-open"
      />
    </label>
  </div>
</div>

{#if inError}
  <div
    id="error-{day}—{dayPeriod}"
    class="mt-s4 flex items-center text-f12 text-error"
  >
    <span class="mr-s4 h-s16 w-s16 fill-current">
      {@html alertIcon}
    </span>
    <span> Horaire incomplète </span>
  </div>
{/if}

<style lang="postcss">
  .error {
    border-color: red;
  }
  .disabled-bg {
    @apply bg-gray-bg;
  }
</style>
