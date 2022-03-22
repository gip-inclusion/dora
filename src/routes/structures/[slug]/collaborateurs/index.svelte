<script context="module">
  import { browser } from "$app/env";
  import { get } from "svelte/store";
  import { userInfo } from "$lib/auth";
  import {
    getStructure,
    getMembers,
    getPutativeMembers,
  } from "$lib/structures";

  export async function load({ params }) {
    // sur le serveur, info est toujours null,
    // on retourne une 404 uniquement sur le client
    if (!browser) {
      return {};
    }

    const info = get(userInfo);

    if (!info) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    const slug = params.slug;
    const structure = await getStructure(slug);
    const isMember = info.structures.some((s) => (s.slug = slug));
    const members = await getMembers(slug);
    const isAdmin = members?.some(
      (m) => m.user.email === info.email && m.isAdmin
    );

    if (!structure || !(isMember || info.isBizdev || info.isStaff)) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    const canSeeMembers = isAdmin || info?.isBizdev || info?.isStaff;
    const putativeMembers = canSeeMembers ? await getPutativeMembers(slug) : [];

    return {
      props: {
        structure,
        members,
        putativeMembers,
        canSeeMembers,
        canEditMembers: isAdmin || info?.isStaff,
        canInviteMembers: isAdmin || info?.isStaff || info?.isBizdev,
      },
    };
  }
</script>

<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import MemberInvited from "./_member_invited.svelte";
  import MemberToConfirm from "./_member_to_confirm.svelte";
  import Button from "$lib/components/button.svelte";
  import AddUserModal from "./_add-user-modal.svelte";
  import MemberStandard from "./_member_standard.svelte";

  export let structure, members, putativeMembers;
  export let canSeeMembers, canEditMembers, canInviteMembers;
  let addUserModalIsOpen = false;

  async function handleRefreshMemberList() {
    members = await getMembers(structure.slug);
    putativeMembers = await getPutativeMembers(structure.slug);
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
  <title>{structure?.name} | Collaborateurs | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <AddUserModal
    bind:isOpen={addUserModalIsOpen}
    {structure}
    {members}
    onRefresh={handleRefreshMemberList}
  />

  <div class="col-span-full md:flex md:items-center md:justify-between">
    <h2 class="mb-s24 text-france-blue">Collaborateurs</h2>

    {#if canInviteMembers}
      <Button
        to={`/structures/${structure.slug}/editer`}
        label="Inviter un collaborateur…"
        small
        on:click={() => (addUserModalIsOpen = true)}
      />
    {/if}
  </div>

  {#if canSeeMembers && members}
    <div class="col-span-full mt-s32 mb-s32 flex flex-col gap-s8">
      {#if putativeMembers}
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
