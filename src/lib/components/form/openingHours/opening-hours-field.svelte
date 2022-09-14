<script lang="ts">
  import Alert from "$lib/components/forms/alert.svelte";

  import type { Day, DayPeriod } from "$lib/types";
  import {
    fromJsonToOsmString,
    getHoursFromStr,
    returnEmptyHoursData,
  } from "$lib/utils/structure";
  import { createEventDispatcher } from "svelte";
  import DayField from "./day-field.svelte";

  export let label: string;
  export let value;
  export let name;
  export let errorMessages: string[];

  const dispatch = createEventDispatcher();

  const data = value ? getHoursFromStr(value) : returnEmptyHoursData();

  function handleHourChange(day: Day, time: DayPeriod) {
    data[day][time].touched = true;
    value = fromJsonToOsmString(data);
    dispatch("change", name);
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

<fieldset>
  <legend class="bold mb-s8 font-bold text-gray-dark first-letter:capitalize">
    {label}
  </legend>

  {#each errorMessages || [] as msg}
    <Alert id="opening-hours-field" label={msg} />
  {/each}

  <div class="mt-s24">
    <div class="day-grid hidden md:block">
      <div>&nbsp;</div>
      <div class="text-center font-bold" aria-hidden="true">Matin</div>
      <div class="text-center font-bold" aria-hidden="true">Après-midi</div>
    </div>

    <!-- Lundi -->
    {#each weekDays as { label, day }}
      <div class="day-grid day">
        <div class="self-center font-bold text-gray-dark">{label}</div>
        <div class="!mb-s10 block text-center font-bold md:hidden">Matin</div>

        <div class="mr-s0 md:mr-s8">
          <DayField
            bind:isOpen={data[day].morning.isOpen}
            bind:touched={data[day].morning.touched}
            bind:openAt={data[day].morning.openAt}
            bind:closeAt={data[day].morning.closeAt}
            label="{label.toLowerCase()} matin"
            {day}
            dayPeriod="morning"
            on:change={() => handleHourChange(day, "morning")}
          />
        </div>
        <div>
          <div class="mb-s10 block text-center font-bold md:hidden">
            Après-midi
          </div>
          <DayField
            bind:isOpen={data[day].afternoon.isOpen}
            bind:openAt={data[day].afternoon.openAt}
            bind:touched={data[day].afternoon.touched}
            bind:closeAt={data[day].afternoon.closeAt}
            label="{label.toLowerCase()}  après-midi"
            {day}
            dayPeriod="afternoon"
            on:change={() => handleHourChange(day, "afternoon")}
          />
        </div>
      </div>
    {/each}
  </div>
</fieldset>

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
