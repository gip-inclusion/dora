<script lang="ts">
  import type { Day } from "$lib/types";
  import {
    getHoursFromStr,
    returnEmptyHoursData,
  } from "$lib/utils/opening-hours/parse";
  import { fromJsonToOsmString } from "$lib/utils/opening-hours/serialize";
  import DayField from "./day-field.svelte";

  interface Props {
    value: string;
    onchange?: (event: Event) => void;
  }

  let { value = $bindable(), onchange }: Props = $props();

  const data = $state(value ? getHoursFromStr(value) : returnEmptyHoursData());

  function handleHourChange(event: Event) {
    value = fromJsonToOsmString(data);
    onchange?.(event);
  }

  const weekDays: { label: string; day: Day }[] = [
    { label: "Lundi", day: "monday" },
    { label: "Mardi", day: "tuesday" },
    { label: "Mercredi", day: "wednesday" },
    { label: "Jeudi", day: "thursday" },
    { label: "Vendredi", day: "friday" },
    { label: "Samedi", day: "saturday" },
    { label: "Dimanche", day: "sunday" },
  ];
</script>

<div class="mt-s24">
  <div class="day-grid hidden md:block">
    <div>&nbsp;</div>
    <div class="text-center font-bold" aria-hidden="true">Plage horaire 1</div>
    <div class="text-center font-bold" aria-hidden="true">Plage horaire 2</div>
  </div>

  <!-- Lundi -->
  {#each weekDays as { label, day }}
    <div class="day-grid day">
      <div class="text-gray-dark self-center font-bold">{label}</div>
      <div class="mb-s10! block text-center font-bold md:hidden">
        Plage horaire 1
      </div>

      <div class="mr-s0 md:mr-s8">
        <DayField
          bind:isOpen={data[day].timeSlot1.isOpen}
          bind:openAt={data[day].timeSlot1.openAt}
          bind:closeAt={data[day].timeSlot1.closeAt}
          label="{label.toLowerCase()} matin ou toute la journée"
          {day}
          dayPeriod="timeSlot1"
          onchange={handleHourChange}
        />
      </div>
      <div>
        <div class="mb-s10 block text-center font-bold md:hidden">
          Plage horaire 2
        </div>
        <DayField
          bind:isOpen={data[day].timeSlot2.isOpen}
          bind:openAt={data[day].timeSlot2.openAt}
          bind:closeAt={data[day].timeSlot2.closeAt}
          label="{label.toLowerCase()} après-midi"
          {day}
          dayPeriod="timeSlot2"
          onchange={handleHourChange}
        />
      </div>
    </div>
  {/each}
</div>

<style lang="postcss">
  @reference "../../../../app.css";

  .day-grid.day > div:first-child {
    grid-column-start: 1;
    grid-column-end: 5;
  }
  .day-grid.day > div {
    margin-bottom: var(--spacing-s24);
  }

  @media (width >= 48rem) {
    .day-grid {
      display: grid;
      grid-template-columns: 1fr 2fr 2fr;
      margin-bottom: var(--spacing-s24);
    }
    .day-grid.day > div:first-child {
      grid-column-start: auto;
      grid-column-end: auto;
    }
  }
</style>
