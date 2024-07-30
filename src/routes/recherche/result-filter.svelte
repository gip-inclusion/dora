<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Checkboxes from "$lib/components/inputs/checkboxes.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import type { Choice } from "$lib/types";

  export let id: string;
  export let label: string;
  export let choices: Array<Choice>;
  export let group: Array<Choice["value"]>;

  const searchText = "";

  function clearSelection() {
    group = [];
  }
</script>

<div class="flex flex-col gap-s16">
  <div
    class="flex items-center justify-between border-b border-b-gray-02 pb-s8"
  >
    <label for={id} class="text-f14 font-bold">{label}</label>
    <Button
      on:click={clearSelection}
      label="Effacer la sélection"
      extraClass={group.length > 0 ? "" : "invisible"}
      noBackground
      noPadding
      small
    />
  </div>
  <div>
    {#if choices.length > 8}
      <Select
        multiple
        extraClass="w-full"
        {id}
        {searchText}
        {choices}
        bind:value={group}
        placeholder="Choisir"
        placeholderMulti="Choisir"
      >
        <Button
          on:click={clearSelection}
          extraClass={`mx-s20 my-s6 ${group.length > 0 ? "" : "hidden"}`}
          label="Effacer la sélection"
          noBackground
          noPadding
          small
          slot="append"
        />
      </Select>
    {:else}
      <Checkboxes name={id} {choices} bind:group />
    {/if}
  </div>
</div>
