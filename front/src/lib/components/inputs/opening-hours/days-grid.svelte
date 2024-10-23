<script lang="ts">
  import type { Day } from "$lib/types";
  import {
    fromJsonToOsmString,
    getHoursFromStr,
    returnEmptyHoursData,
  } from "$lib/utils/opening-hours";
  import { createEventDispatcher } from "svelte";
  import DayField from "./day-field.svelte";

  export let id: string;
  export let value;

  const dispatch = createEventDispatcher();

  const data = value ? getHoursFromStr(value) : returnEmptyHoursData();

  function handleHourChange() {
    value = fromJsonToOsmString(data);
    dispatch("change", id);
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
      <div class="self-center font-bold text-gray-dark">{label}</div>
      <div class="!mb-s10 block text-center font-bold md:hidden">
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
          on:change={() => handleHourChange()}
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
          on:change={() => handleHourChange()}
        />
      </div>
    </div>
  {/each}
</div>

<style lang="postcss">
  .day-grid.day > div:first-child {
    grid-column-start: 1;
    grid-column-end: 5;
  }
  .day-grid.day > div {
    @apply mb-s24;
  }

  @screen md {
    .day-grid {
      display: grid;
      grid-template-columns: 1fr 2fr 2fr;
      @apply mb-s24;
    }
    .day-grid.day > div:first-child {
      grid-column-start: auto;
      grid-column-end: auto;
    }
  }
</style>
