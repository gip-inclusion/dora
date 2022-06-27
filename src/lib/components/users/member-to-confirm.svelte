<script>
  import Button from "$lib/components/button.svelte";
  import Label from "$lib/components/label.svelte";

  import { fileEditIcon, fileForbidIcon, userIcon } from "$lib/icons";
  import { rejectMembershipRequest, acceptMember } from "$lib/structures";
  import Member from "./member.svelte";

  export let member;
  export let onRefresh;
  export let readOnly = false;

  $: userLevel = member.isAdmin ? "Admin" : "Utilisateur";

  async function handleAcceptRequest() {
    await acceptMember(member.id);
    await onRefresh();
  }

  async function handleCancelRequest() {
    if (confirm(`Refuser la requête de ${member.user.fullName} ?`)) {
      await rejectMembershipRequest(member.id);
      await onRefresh();
    }
  }
</script>

<Member {member} {readOnly}>
  <div slot="label">
    <Label
      label={`${userLevel} – Adhésion en attente`}
      smallIcon
      icon={userIcon}
      wait
    />
  </div>

  <div slot="actions" let:onCloseParent>
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
  </div>
</Member>
