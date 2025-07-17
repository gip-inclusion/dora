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

  interface Props {
    member: any;
    onRefresh: any;
    readOnly?: boolean;
  }

  let { member, onRefresh, readOnly = false }: Props = $props();

  let userLevel = $derived(member.isAdmin ? "Admin" : "Utilisateur");
  let userLevelIcon = $derived(member.isAdmin ? user2Icon : userIcon);

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
  {#snippet label()}
    <div>
      <Label label={userLevel} smallIcon icon={userLevelIcon} />
    </div>
  {/snippet}
  {#snippet status()}
    <div>
      <span
        class="bg-service-orange px-s12 py-s6 inline-block rounded-lg text-center"
      >
        Adhésion en attente
      </span>
    </div>
  {/snippet}

  {#snippet actions({ onCloseParent })}
    <div>
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
  {/snippet}
</Member>
