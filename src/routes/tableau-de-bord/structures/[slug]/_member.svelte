<script>
  import ButtonMenu from "$lib/components/button-menu.svelte";

  import { moreIcon } from "$lib/icons";

  export let member;
  export let isMyself = false;
  export let isOnlyAdmin = false;
  export let readOnly = false;
</script>

<div class="wrapper" class:is-own={isMyself}>
  <div class="flex flex-col">
    <h5>{member.user.fullName}</h5>
    <div class="text-f14 text-gray-text-alt">{member.user.email}</div>
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
  .wrapper {
    display: flex;
    align-items: center;
    padding: 6px 16px;
    background-color: var(--col-white);
    border-radius: var(--s8);
    box-shadow: var(--shadow-sm);
    gap: var(--s16);
  }

  .is-own {
    background-color: var(--col-gray-01);
  }
</style>
