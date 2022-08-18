<script context="module">
  import { browser } from "$app/env";
  import { get } from "svelte/store";
  import { userInfo } from "$lib/auth";
  import { structure } from "../_store";

  import { getMembers, getPutativeMembers } from "$lib/structures";

  export async function load({ fetch }) {
    // sur le serveur, info est toujours null,
    // on retourne une 404 uniquement sur le client
    if (!browser) {
      return {};
    }

    const info = get(userInfo);
    const struct = get(structure);

    const canSeeMembers = struct.isMember || info?.isBizdev || info?.isStaff;
    const canEditMembers = struct.isAdmin || info?.isBizdev || info?.isStaff;

    if (!info || !struct || !canSeeMembers) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    const members = await getMembers(struct.slug, { kitFetch: fetch });
    const putativeMembers = await getPutativeMembers(struct.slug, {
      kitFetch: fetch,
    });

    return {
      props: {
        members,
        putativeMembers,
        canSeeMembers,
        canEditMembers,
      },
    };
  }
</script>

<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import Button from "$lib/components/button.svelte";
  import MemberInvited from "$lib/components/users/member-invited.svelte";
  import MemberToConfirm from "$lib/components/users/member-to-confirm.svelte";
  import MemberStandard from "$lib/components/users/member-standard.svelte";
  import ModalAddUser from "$lib/components/users/modal-add-user.svelte";

  export let members, putativeMembers, canSeeMembers, canEditMembers;

  let modalAddUserIsOpen = false;

  async function handleRefreshMemberList() {
    members = await getMembers($structure.slug);
    putativeMembers = await getPutativeMembers($structure.slug);
  }

  function sortedMembers(items) {
    return items.sort((a, b) => {
      if (a.isAdmin && !b.isAdmin) return -1;
      if (!a.isAdmin && b.isAdmin) return 1;
      const lA = a.user.lastName || a.user.email;
      const lB = b.user.lastName || b.user.email;
      return lA.localeCompare(lB, "fr");
    });
  }
</script>

<svelte:head>
  <title>{$structure?.name} | Collaborateurs | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  {#if canEditMembers}
    <ModalAddUser
      bind:isOpen={modalAddUserIsOpen}
      structure={$structure}
      {members}
      onRefresh={handleRefreshMemberList}
    />
  {/if}

  <div class="md:flex md:items-center md:justify-between">
    <h2 class="text-france-blue">Collaborateurs</h2>
    {#if canEditMembers}
      <Button
        label="Inviter un collaborateur"
        small
        on:click={() => (modalAddUserIsOpen = true)}
      />
    {/if}
  </div>

  {#if canSeeMembers}
    <div class="mt-s32 mb-s32 flex flex-col gap-s8">
      {#if canEditMembers && putativeMembers}
        {#each sortedMembers(putativeMembers) as member}
          {#if member.invitedByAdmin}
            <MemberInvited
              {member}
              onRefresh={handleRefreshMemberList}
              readOnly={!canEditMembers}
            />
          {:else}
            <MemberToConfirm
              {member}
              onRefresh={handleRefreshMemberList}
              readOnly={!canEditMembers}
            />
          {/if}
        {/each}
      {/if}
      {#each sortedMembers(members) as member}
        <MemberStandard
          {member}
          onRefresh={handleRefreshMemberList}
          isMyself={member.user.email === $userInfo.email}
          isOnlyAdmin={member.user.email === $userInfo.email &&
            members.filter((m) => m.isAdmin).length === 1}
          readOnly={!canEditMembers}
        />
      {/each}
    </div>
  {/if}
</EnsureLoggedIn>
