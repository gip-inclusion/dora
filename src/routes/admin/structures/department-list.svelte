<script lang="ts">
  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import Button from "$lib/components/display/button.svelte";
  import { arrowDownSIcon } from "$lib/icons";

  // on pourrait affiner les types, mais ça alourdirait de beaucoup
  export let departments;
  export let selectedDepartment;
  export let onRefresh;
</script>

<ButtonMenu
  label="{selectedDepartment.name} ({selectedDepartment.code})"
  icon={arrowDownSIcon}
  iconOnRight
  big
  noPadding
  extraClass="!text-france-blue"
  alignRight={false}
  let:onClose={onCloseParent}
>
  <div class="flex flex-col items-start gap-s12 px-s12 py-s12 !text-gray-dark">
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
        extraClass="!text-gray-dark !font-normal"
      />
    {/each}
  </div>
</ButtonMenu>
