<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import Label from "$lib/components/display/label.svelte";
  import { userIcon, user2Icon, settingsIcon, forbidIcon } from "$lib/icons";
  import { deleteMember } from "$lib/requests/structures";
  import { refreshUserInfo } from "$lib/utils/auth";
  import Member from "./member.svelte";
  import ModalChangeUser from "./modal-change-user.svelte";

  export let member;
  export let onRefresh;
  export let readOnly = true;
  export let structureSlug: string;
  export let isMyself;

  let modalChangeUserIsOpen = false;
  $: userLevel = member.isAdmin ? "Admin" : "Utilisateur";
  $: userLevelIcon = member.isAdmin ? user2Icon : userIcon;

  async function handleDelete() {
    const confirmText = isMyself
      ? "Quitter la structure ?"
      : `Supprimer l’utilisateur ${member.user.fullName} ?`;

    if (confirm(confirmText)) {
      await deleteMember(member.id);
      if (isMyself) {
        await refreshUserInfo();
        // Force la réactualisation de toute la structure
        goto(`/structures/${structureSlug}`);
      } else {
        await onRefresh();
      }
    }
  }
</script>

<ModalChangeUser bind:isOpen={modalChangeUserIsOpen} bind:member {onRefresh} />
<Member {member} {isMyself} {readOnly}>
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
    <div>
      <Button
        label={isMyself ? "Quitter la structure" : "Révoquer"}
        on:click={() => {
          handleDelete();
          onCloseParent();
        }}
        icon={forbidIcon}
        iconOnRight
        small
        extraClass="justify-end whitespace-nowrap"
        noBackground
      />
    </div>
  </div>
</Member>
