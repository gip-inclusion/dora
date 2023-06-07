<script lang="ts">
  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import { moreIcon } from "$lib/icons";

  export let member;
  export let isMyself = false;
  export let readOnly = false;
</script>

<div
  class="flex flex-col justify-between gap-s16 rounded-md border border-gray-01 py-s16 px-s24 md:flex-row md:items-center"
>
  <div class="flex flex-1 flex-col">
    <h4>{member.user.fullName}</h4>
    <p class="mb-s0 text-f14 text-gray-text">{member.user.email}</p>
  </div>

  <div class="flex flex-1 flex-wrap items-center gap-x-s32 text-f14">
    <div class="flex-[3] text-center md:text-right">
      {#if isMyself}
        <span class="rounded-md bg-magenta-10 py-s6 px-s12">Vous</span>
      {/if}
      <slot name="status" />
    </div>
    <div class="flex-[2]">
      <slot name="label" />
    </div>
    <div class="flex-1">
      {#if !readOnly}
        <ButtonMenu small icon={moreIcon} let:onClose={onCloseParent}>
          <slot name="actions" {onCloseParent} />
        </ButtonMenu>
      {/if}
    </div>
  </div>
</div>
