<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Label from "$lib/components/display/label.svelte";
  import { userIcon, user2Icon, forbidIcon, repeatIcon } from "$lib/icons";
  import { cancelInvite, resendInvite } from "$lib/requests/structures";
  import Member from "./member.svelte";

  interface Props {
    member: any;
    onRefresh: any;
    readOnly?: boolean;
  }

  let { member, onRefresh, readOnly = false }: Props = $props();

  let userLevel = $derived(member.isAdmin ? "Admin" : "Utilisateur");
  let userLevelIcon = $derived(member.isAdmin ? user2Icon : userIcon);

  async function handleCancelInvite() {
    if (
      confirm(
        `Souhaitez-vous annuler votre invitation à l’utilisateur “${member.user.fullName}” ?`
      )
    ) {
      await cancelInvite(member.id);
      await onRefresh();
    }
  }

  async function handleResendInvite() {
    await resendInvite(member.id);
  }
</script>

<Member {member} {readOnly}>
  {#snippet label()}
    <div >
      <Label label={userLevel} smallIcon icon={userLevelIcon} />
    </div>
  {/snippet}
  {#snippet status()}
    <div >
      <span
        class="bg-blue-light px-s12 py-s6 inline-block rounded-lg text-center"
      >
        Invitation envoyée
      </span>
    </div>
  {/snippet}

  {#snippet actions({ onCloseParent })}
    <div  >
      <div class="flex flex-col items-end">
        <Button
          label="Relancer"
          on:click={() => {
            handleResendInvite();
            onCloseParent();
          }}
          icon={repeatIcon}
          iconOnRight
          small
          noBackground
        />

        <Button
          label="Révoquer"
          on:click={() => {
            handleCancelInvite();
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
