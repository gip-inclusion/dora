<script lang="ts">
  import ArrowDownSLineArrows from "svelte-remix/ArrowDownSLineArrows.svelte";

  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import Button from "$lib/components/display/button.svelte";
  import type { GeoApiValue } from "$lib/types";

  interface Props {
    departments: { value: GeoApiValue; label: string }[];
    selectedDepartment: GeoApiValue;
    onChange: (department: GeoApiValue) => void;
  }

  let { departments, selectedDepartment, onChange }: Props = $props();
</script>

<ButtonMenu
  label="{selectedDepartment.name} ({selectedDepartment.code})"
  icon={ArrowDownSLineArrows}
  iconOnRight
  big
  noPadding
  extraClass="text-france-blue!"
  alignRight={false}
>
  {#snippet children({ onClose: onCloseParent })}
    <div
      class="gap-s12 px-s12 py-s12 text-gray-dark! flex flex-col items-start"
    >
      {#each departments as dpt}
        <Button
          onclick={() => {
            onChange(dpt.value);
            onCloseParent();
          }}
          label={dpt.label}
          small
          noWrap
          noBackground
          extraClass="text-gray-dark! font-normal!"
        />
      {/each}
    </div>
  {/snippet}
</ButtonMenu>
