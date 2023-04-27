<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Label from "$lib/components/display/label.svelte";
  import { userIcon, user2Icon, settingsIcon, forbidIcon } from "$lib/icons";
  import { deleteMember } from "$lib/requests/structures";
  import Member from "./member.svelte";
  import ModalChangeUser from "./modal-change-user.svelte";

  export let member;
  export let onRefresh;
  export let readOnly = true;
  export let isMyself, isOnlyAdmin;

  let modalChangeUserIsOpen = false;
  $: userLevel = member.isAdmin ? "Admin" : "Utilisateur";
  $: userLevelIcon = member.isAdmin ? user2Icon : userIcon;

  async function handleDelete() {
    if (confirm(`Supprimer l’utilisateur ${member.user.fullName} ?`)) {
      await deleteMember(member.id);
      await onRefresh();
    }
  }
</script>

<ModalChangeUser bind:isOpen={modalChangeUserIsOpen} bind:member {onRefresh} />
<Member {isOnlyAdmin} {member} {isMyself} {readOnly}>
  <div slot="label">
    <Label label={userLevel} smallIcon icon={userLevelIcon} />
  </div>

  <div slot="actions" let:onCloseParent>
    <div>
      <Button
        label="Modifier"
        on:click={() => {
          modalChangeUserIsOpen = true;
          onCloseParent();
        }}
        icon={settingsIcon}
        iconOnRight
        small
        wFull
        extraClass="justify-end"
        noBackground
      />
    </div>
    {#if !isMyself}
      <div>
        <Button
          label="Révoquer"
          on:click={() => {
            handleDelete();
            onCloseParent();
          }}
          icon={forbidIcon}
          iconOnRight
          small
          extraClass="justify-end"
          noBackground
        />
      </div>
    {/if}
  </div>
</Member>
