<script lang="ts">
  import UserLineUserFaces from "svelte-remix/UserLineUserFaces.svelte";
  import User2LineUserFaces from "svelte-remix/User2LineUserFaces.svelte";
  import Forbid2LineSystem from "svelte-remix/Forbid2LineSystem.svelte";
  import CheckboxCircleLineSystem from "svelte-remix/CheckboxCircleLineSystem.svelte";

  import Button from "$lib/components/display/button.svelte";
  import Label from "$lib/components/display/label.svelte";
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
  let userLevelIcon = $derived(
    member.isAdmin ? User2LineUserFaces : UserLineUserFaces
  );

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
          onclick={() => {
            handleAcceptRequest();
            onCloseParent();
          }}
          icon={CheckboxCircleLineSystem}
          iconOnRight
          small
          noBackground
        />

        <Button
          label="Révoquer"
          onclick={() => {
            handleCancelRequest();
            onCloseParent();
          }}
          icon={Forbid2LineSystem}
          iconOnRight
          small
          noBackground
        />
      </div>
    </div>
  {/snippet}
</Member>
