<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Label from "$lib/components/display/label.svelte";
  import { userIcon, user2Icon, forbidIcon, repeatIcon } from "$lib/icons";
  import { cancelInvite, resendInvite } from "$lib/requests/structures";
  import Member from "./member.svelte";

  export let member;
  export let onRefresh;
  export let readOnly = false;

  $: userLevel = member.isAdmin ? "Admin" : "Utilisateur";
  $: userLevelIcon = member.isAdmin ? user2Icon : userIcon;

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
  <div slot="label">
    <Label label={userLevel} smallIcon icon={userLevelIcon} />
  </div>
  <div slot="status">
    <span
      class="inline-block rounded-md bg-blue-light py-s6 px-s12 text-center"
    >
      Invitation envoyée
    </span>
  </div>

  <div slot="actions" let:onCloseParent>
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
  </div></Member
>
