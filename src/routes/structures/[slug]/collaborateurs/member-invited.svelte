<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Label from "$lib/components/display/label.svelte";
  import { fileEditIcon, fileForbidIcon, userIcon } from "$lib/icons";
  import { cancelInvite, resendInvite } from "$lib/requests/structures";
  import Member from "./member.svelte";

  export let member;
  export let onRefresh;
  export let readOnly = false;

  $: userLevel = member.isAdmin ? "Admin" : "Utilisateur";

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
    <Label
      label={`${userLevel} – Invitation envoyée`}
      smallIcon
      icon={userIcon}
      light
    />
  </div>

  <div slot="actions" let:onCloseParent>
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
  </div>
</Member>
