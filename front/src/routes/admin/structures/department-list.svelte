<script lang="ts">
  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import Button from "$lib/components/display/button.svelte";
  import { arrowDownSIcon } from "$lib/icons";

  
  interface Props {
    // on pourrait affiner les types, mais ça alourdirait de beaucoup
    departments: any;
    selectedDepartment: any;
    onRefresh: any;
  }

  let { departments, selectedDepartment, onRefresh }: Props = $props();
</script>

<ButtonMenu
  label="{selectedDepartment.name} ({selectedDepartment.code})"
  icon={arrowDownSIcon}
  iconOnRight
  big
  noPadding
  extraClass="text-france-blue!"
  alignRight={false}
  
>
  {#snippet children({ onClose: onCloseParent })}
    <div class="gap-s12 px-s12 py-s12 text-gray-dark! flex flex-col items-start">
      {#each departments as dpt}
        <Button
          on:click={() => {
            onRefresh(dpt.value);
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
