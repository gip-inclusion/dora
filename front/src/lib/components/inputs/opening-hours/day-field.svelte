<script lang="ts">
  import { alertIcon } from "$lib/icons";
  import type { Day, DayPeriod } from "$lib/types";
  import Toggle from "./toggle.svelte";

  interface Props {
    label: string;
    isOpen: boolean;
    openAt: string;
    closeAt: string;
    day: Day;
    dayPeriod: DayPeriod;
    onchange?: (event: Event) => void;
  }

  let {
    label,
    isOpen = $bindable(),
    openAt = $bindable(),
    closeAt = $bindable(),
    day,
    dayPeriod,
    onchange,
  }: Props = $props();

  let inError = $derived(
    isOpen && (closeAt || openAt) && (!closeAt || !openAt || openAt >= closeAt)
  );

  let ariaDescribedBy = $derived(
    inError ? `error-${day}—${dayPeriod}` : undefined
  );

  function handleUpdate(event: Event) {
    // Clear values and notify change
    if (!isOpen) {
      openAt = "";
      closeAt = "";
    }
    onchange?.(event);
  }
</script>

<div class:disabled-bg={!isOpen}>
  <div
    class="border-gray-03 text-gray-text flex w-full justify-around rounded-tl rounded-tr border text-center"
    class:error={inError}
  >
    <span class="border-gray-03 py-s10 text-f18 flex-1 border-r">
      {#if !isOpen}
        <span class="text-f19 text-gray-text-alt">/</span>
      {:else}
        <label class:error={inError}>
          <span class="sr-only">Horaire d’ouverture pour le {label}</span>
          <input
            {onchange}
            bind:value={openAt}
            type="time"
            aria-describedby={ariaDescribedBy}
          />
        </label>
      {/if}
    </span>

    <span class="border-gray-03 py-s10 text-f18 flex-1">
      {#if !isOpen}
        <span class="text-f19 text-gray-text-alt">/</span>
      {:else}
        <label class="py-s10 flex-1">
          <span class="sr-only">Horaire de fermeture pour le {label}</span>

          <input
            {onchange}
            bind:value={closeAt}
            disabled={!isOpen}
            class:disabled-bg={!isOpen}
            type="time"
            max="24"
          />
        </label>
      {/if}
    </span>
  </div>

  <div
    class="border-gray-03 py-s10 text-gray-text flex flex-row justify-center rounded-br rounded-bl border-r border-b border-l text-center"
    class:error={inError}
  >
    <label for="{day}-{dayPeriod}-is-open" class="flex justify-center">
      <span class="sr-only">
        {dayPeriod === "timeSlot1"
          ? "Ouvrir sur une première plage horaire"
          : "Ouvrir une seconde plage horaire"}
      </span>
    </label>
    <Toggle
      onchange={(event) => handleUpdate(event)}
      bind:checked={isOpen}
      yesLabel="Ouvert"
      noLabel="Fermé"
      id="{day}-{dayPeriod}-is-open"
    />
  </div>
</div>

{#if inError}
  <div
    id="error-{day}—{dayPeriod}"
    class="mt-s4 text-f12 text-error flex items-center"
  >
    <span class="mr-s4 h-s16 w-s16 fill-current">
      {@html alertIcon}
    </span>
    <span>Horaire incomplet ou incohérent.</span>
  </div>
{/if}

<style lang="postcss">
  @reference "../../../../app.css";

  .error {
    border-color: red;
  }
  .disabled-bg {
    @apply bg-gray-bg;
  }
</style>
