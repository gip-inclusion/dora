<script>
  // import { userInfo } from "$lib/auth";

  import ButtonMenu from "$lib/components/button-menu.svelte";
  import Button from "$lib/components/button.svelte";
  import Label from "$lib/components/label.svelte";

  import { fileEditIcon, fileForbidIcon, userIcon, moreIcon } from "$lib/icons";
  import { deleteMember, resendInvite } from "$lib/structures";
  import ChangeUserModal from "./_change-user-modal.svelte";

  export let member;
  export let onRefresh;
  export let isMyself, isOnlyAdmin;

  let changeUserModalIsOpen = false;
  let flashInviteButtonSuccess = false;
  $: userLevel = member.isAdmin ? "Admin" : "Utilisateur";
  async function handleDelete() {
    if (confirm(`Supprimer l’utilisateur ${member.user.fullName} ?`)) {
      await deleteMember(member.id);
      await onRefresh();
    }
  }
  async function handleResendInvite() {
    flashInviteButtonSuccess = true;
    await resendInvite(member.id);
    flashInviteButtonSuccess = false;
  }
</script>

<style>
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

<ChangeUserModal bind:isOpen={changeUserModalIsOpen} bind:member {onRefresh} />
<div class="wrapper" class:is-own={isMyself}>
  <h5>{member.user.fullName}</h5>
  <div class="grow">
    {#if !member.hasAcceptedInvitation || member.mustSetPassword}
      <div class="flex items-baseline">
        <div class="legend-xs text-gray-text-alt">Invitation envoyée</div>
        <Button
          label="Renvoyer"
          noBackground
          small
          flashSuccess={flashInviteButtonSuccess}
          disabled={flashInviteButtonSuccess}
          on:click={handleResendInvite}
        />
      </div>
    {/if}
  </div>
  <div class="grow" />
  <Label label={userLevel} smallIcon iconOnLeft icon={userIcon} />
  <div>
    <ButtonMenu
      icon={moreIcon}
      let:onClose={onCloseParent}
      disabled={isOnlyAdmin}
    >
      <div>
        <Button
          label="Modifier"
          on:click={() => {
            changeUserModalIsOpen = true;
            onCloseParent();
          }}
          icon={fileEditIcon}
          iconOnRight
          small
          noBackground
        />
      </div>
      {#if !isMyself}
        <div>
          <Button
            label="Supprimer"
            on:click={() => {
              handleDelete();
              onCloseParent();
            }}
            icon={fileForbidIcon}
            iconOnRight
            small
            noBackground
          />
        </div>
      {/if}
    </ButtonMenu>
  </div>
</div>
