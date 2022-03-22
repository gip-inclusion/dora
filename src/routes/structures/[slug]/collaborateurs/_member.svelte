<script>
  import ButtonMenu from "$lib/components/button-menu.svelte";

  import { moreIcon } from "$lib/icons";

  export let member;
  export let isMyself = false;
  export let isOnlyAdmin = false;
  export let readOnly = false;
</script>

<div
  class="flex items-center gap-s16 rounded-md border border-gray-01 py-s16 px-s24"
  class:is-own={isMyself}
>
  <div class="flex flex-col">
    <h4>{member.user.fullName}</h4>
    <p class="mb-s0 text-f14 text-gray-text-alt">{member.user.email}</p>
  </div>
  <div class="grow" />
  <slot name="label" />

  {#if !readOnly}
    <div>
      <ButtonMenu
        icon={moreIcon}
        let:onClose={onCloseParent}
        disabled={isOnlyAdmin}
      >
        <slot name="actions" {onCloseParent} />
      </ButtonMenu>
    </div>
  {/if}
</div>

<style lang="postcss">
  .is-own {
    background-color: var(--col-gray-01);
  }
</style>
