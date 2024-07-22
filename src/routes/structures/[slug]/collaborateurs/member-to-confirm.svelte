<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Label from "$lib/components/display/label.svelte";
  import {
    userIcon,
    user2Icon,
    forbidIcon,
    checkboxCircleIcon,
  } from "$lib/icons";
  import {
    acceptMember,
    rejectMembershipRequest,
  } from "$lib/requests/structures";
  import Member from "./member.svelte";

  export let member;
  export let onRefresh;
  export let readOnly = false;

  $: userLevel = member.isAdmin ? "Admin" : "Utilisateur";
  $: userLevelIcon = member.isAdmin ? user2Icon : userIcon;

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
    <Label label={userLevel} smallIcon icon={userLevelIcon} />
  </div>
  <div slot="status">
    <span
      class="inline-block rounded-md bg-service-orange px-s12 py-s6 text-center"
    >
      Adhésion en attente
    </span>
  </div>

  <div slot="actions" let:onCloseParent>
    <div class="flex flex-col items-end">
      <Button
        label="Accepter"
        on:click={() => {
          handleAcceptRequest();
          onCloseParent();
        }}
        icon={checkboxCircleIcon}
        iconOnRight
        small
        noBackground
      />

      <Button
        label="Révoquer"
        on:click={() => {
          handleCancelRequest();
          onCloseParent();
        }}
        icon={forbidIcon}
        iconOnRight
        small
        noBackground
      />
    </div>
  </div>
</Member>
