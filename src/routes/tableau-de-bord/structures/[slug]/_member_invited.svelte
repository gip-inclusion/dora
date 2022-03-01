<script>
  import Button from "$lib/components/button.svelte";
  import Label from "$lib/components/label.svelte";

  import { fileEditIcon, fileForbidIcon, userIcon } from "$lib/icons";
  import { resendInvite, cancelInvite } from "$lib/structures";
  import Member from "./_member.svelte";

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
