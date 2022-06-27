<script>
  import Button from "$lib/components/button.svelte";
  import Label from "$lib/components/label.svelte";

  import { fileEditIcon, fileForbidIcon, userIcon } from "$lib/icons";
  import { deleteMember } from "$lib/structures";
  import ModalChangeUser from "./modal-change-user.svelte";
  import Member from "./member.svelte";

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
