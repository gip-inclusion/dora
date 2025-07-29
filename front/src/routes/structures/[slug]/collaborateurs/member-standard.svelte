<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import Label from "$lib/components/display/label.svelte";
  import { userIcon, user2Icon, settingsIcon, forbidIcon } from "$lib/icons";
  import { deleteMember } from "$lib/requests/structures";
  import { refreshUserInfo } from "$lib/utils/auth";
  import Member from "./member.svelte";
  import ModalChangeUser from "./modal-change-user.svelte";

  interface Props {
    member: any;
    onRefresh: any;
    readOnly?: boolean;
    structureSlug: string;
    isMyself: any;
  }

  let {
    member = $bindable(),
    onRefresh,
    readOnly = true,
    structureSlug,
    isMyself,
  }: Props = $props();

  let modalChangeUserIsOpen = $state(false);
  let userLevel = $derived(member.isAdmin ? "Admin" : "Utilisateur");
  let userLevelIcon = $derived(member.isAdmin ? user2Icon : userIcon);

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
  {#snippet label()}
    <div>
      <Label label={userLevel} smallIcon icon={userLevelIcon} />
    </div>
  {/snippet}

  {#snippet actions({ onCloseParent })}
    <div>
      <div class="flex flex-col items-end">
        <Button
          label="Modifier"
          onclick={() => {
            modalChangeUserIsOpen = true;
            onCloseParent();
          }}
          icon={settingsIcon}
          iconOnRight
          small
          noBackground
        />

        <Button
          label={isMyself ? "Quitter la structure" : "Révoquer"}
          onclick={() => {
            handleDelete();
            onCloseParent();
          }}
          icon={forbidIcon}
          iconOnRight
          small
          noBackground
        />
      </div>
    </div>
  {/snippet}</Member
>
