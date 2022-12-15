<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Label from "$lib/components/display/label.svelte";
  import { fileEditIcon, fileForbidIcon, userIcon } from "$lib/icons";
  import { deleteMember } from "$lib/requests/structures";
  import Member from "./member.svelte";
  import ModalChangeUser from "./modal-change-user.svelte";

  export let member;
  export let onRefresh;
  export let readOnly = true;
  export let isMyself, isOnlyAdmin;

  let modalChangeUserIsOpen = false;
  $: userLevel = member.isAdmin ? "Admin" : "Utilisateur";
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
    <Label label={userLevel} smallIcon icon={userIcon} />
  </div>

  <div slot="actions" let:onCloseParent>
    <div>
      <Button
        label="Modifier"
        on:click={() => {
          modalChangeUserIsOpen = true;
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
  </div>
</Member>
