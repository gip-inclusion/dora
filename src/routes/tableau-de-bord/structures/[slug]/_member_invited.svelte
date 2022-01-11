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

  let changeUserModalIsOpen = false;
  $: userLevel = member.isAdmin ? "Admin" : "Utilisateur";
  async function handleCancelInvite() {
    if (confirm(`Supprimer l’utilisateur ${member.user.fullName} ?`)) {
      await deleteMember(member.id);
      await onRefresh();
    }
  }
  async function handleResendInvite() {
    await resendInvite(member.id);
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
<div class="wrapper">
  <div class="flex flex-col">
    <h5>{member.user.fullName}</h5>
    <div class="text-gray-text-alt text-f14">{member.user.email}</div>
  </div>
  <div class="grow" />
  <Label
    label={`${userLevel} – Invitation envoyée`}
    smallIcon
    iconOnLeft
    icon={userIcon}
    light
  />
  <div>
    <ButtonMenu icon={moreIcon} let:onClose={onCloseParent}>
      <div>
        <Button
          label="Relancer"
          on:click={() => {
            handleResendInvite();
            onCloseParent();
          }}
          icon={fileEditIcon}
          iconOnRight
          small
          noBackground
        />
      </div>
      <div>
        <Button
          label="Révoquer"
          on:click={() => {
            handleCancelInvite();
            onCloseParent();
          }}
          icon={fileForbidIcon}
          iconOnRight
          small
          noBackground
        />
      </div>
    </ButtonMenu>
  </div>
</div>
