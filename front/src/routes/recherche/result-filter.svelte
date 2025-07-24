<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Checkboxes from "$lib/components/inputs/checkboxes.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import type { Choice } from "$lib/types";

  interface Props {
    id: string;
    label: string;
    choices: Array<Choice>;
    group: Array<Choice["value"]>;
  }

  let { id, label, choices, group = $bindable() }: Props = $props();

  const searchText = "";

  function clearSelection() {
    group = [];
  }
</script>

<div class="gap-s16 flex flex-col">
  <div
    class="border-b-gray-02 pb-s8 flex items-center justify-between border-b"
  >
    <label for={id} class="text-f14 font-bold">{label}</label>
    <Button
      onclick={clearSelection}
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
        {#snippet append()}
          <Button
            onclick={clearSelection}
            extraClass={`mx-s20 my-s6 ${group.length > 0 ? "" : "hidden"}`}
            label="Effacer la sélection"
            noBackground
            noPadding
            small
          />
        {/snippet}
      </Select>
    {:else}
      <Checkboxes name={id} {choices} bind:group />
    {/if}
  </div>
</div>
