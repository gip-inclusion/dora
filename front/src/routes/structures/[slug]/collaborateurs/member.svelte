<script lang="ts">
  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import { moreIcon } from "$lib/icons";

  export let member;
  export let isMyself = false;
  export let readOnly = false;
</script>

<div
  class="gap-s16 border-gray-01 px-s24 py-s16 flex flex-col justify-between rounded-lg border md:flex-row md:items-center"
>
  <div class="flex flex-1 flex-col">
    <h4>{member.user.fullName}</h4>
    <p class="mb-s0 text-f14 text-gray-text">{member.user.email}</p>
  </div>

  <div class="gap-x-s32 text-f14 flex flex-1 flex-wrap items-center">
    <div class="flex-3 text-center md:text-right">
      {#if isMyself}
        <span class="bg-magenta-10 px-s12 py-s6 rounded-lg">Vous</span>
      {/if}
      <slot name="status" />
    </div>
    <div class="flex-2">
      <slot name="label" />
    </div>
    <div class="flex-1">
      {#if !readOnly}
        <ButtonMenu
          small
          icon={moreIcon}
          let:onClose={onCloseParent}
          hideLabel
          label="Actions disponibles pour l'utilisateur"
        >
          <slot name="actions" {onCloseParent} />
        </ButtonMenu>
      {/if}
    </div>
  </div>
</div>
