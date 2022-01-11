<script>
  // import { userInfo } from "$lib/auth";

  import ButtonMenu from "$lib/components/button-menu.svelte";
  import Button from "$lib/components/button.svelte";
  import Label from "$lib/components/label.svelte";

  import { fileEditIcon, fileForbidIcon, userIcon, moreIcon } from "$lib/icons";
  import { deleteMember, acceptMember } from "$lib/structures";
  import ChangeUserModal from "./_change-user-modal.svelte";

  export let member;
  export let onRefresh;

  let changeUserModalIsOpen = false;
  $: userLevel = member.isAdmin ? "Admin" : "Utilisateur";

  async function handleAcceptRequest() {
    await acceptMember(member.id);
    await onRefresh();
  }

  async function handleCancelRequest() {
    if (confirm(`Supprimer l’utilisateur ${member.user.fullName} ?`)) {
      await deleteMember(member.id);
      await onRefresh();
    }
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
</style>

<ChangeUserModal bind:isOpen={changeUserModalIsOpen} bind:member {onRefresh} />
<div class="wrapper">
  <div class="flex flex-col">
    <h5>{member.user.fullName}</h5>
    <div class="text-gray-text-alt text-f14">{member.user.email}</div>
  </div>

  <div class="grow" />
  <Label
    label={`${userLevel} – Adhésion en attente`}
    smallIcon
    iconOnLeft
    icon={userIcon}
    wait
  />
  <div>
    <ButtonMenu icon={moreIcon} let:onClose={onCloseParent}>
      <div>
        <Button
          label="Accepter"
          on:click={() => {
            handleAcceptRequest();
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
            handleCancelRequest();
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
