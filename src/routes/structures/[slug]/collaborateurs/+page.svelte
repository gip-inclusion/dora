<script lang="ts">
  import { userInfo } from "$lib/auth";
  import Button from "$lib/components/button.svelte";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import MemberInvited from "$lib/components/users/member-invited.svelte";
  import MemberStandard from "$lib/components/users/member-standard.svelte";
  import MemberToConfirm from "$lib/components/users/member-to-confirm.svelte";
  import ModalAddUser from "$lib/components/users/modal-add-user.svelte";
  import { getMembers, getPutativeMembers } from "$lib/structures";
  import { structure } from "../_store";
  import type { PageData } from "./$types";

  export let data: PageData;

  let modalAddUserIsOpen = false;

  async function handleRefreshMemberList() {
    data.members = await getMembers($structure.slug);
    data.putativeMembers = await getPutativeMembers($structure.slug);
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
  {#if data.canEditMembers}
    <ModalAddUser
      bind:isOpen={modalAddUserIsOpen}
      structure={$structure}
      members={data.members}
      onRefresh={handleRefreshMemberList}
    />
  {/if}

  <div class="md:flex md:items-center md:justify-between">
    <h2 class="text-france-blue">Collaborateurs</h2>
    {#if data.canEditMembers}
      <Button
        label="Inviter un collaborateur"
        small
        on:click={() => (modalAddUserIsOpen = true)}
      />
    {/if}
  </div>

  {#if data.canSeeMembers}
    <div class="mt-s32 mb-s32 flex flex-col gap-s8">
      {#if data.canEditMembers && data.putativeMembers}
        {#each sortedMembers(data.putativeMembers) as member}
          {#if member.invitedByAdmin}
            <MemberInvited
              {member}
              onRefresh={handleRefreshMemberList}
              readOnly={!data.canEditMembers}
            />
          {:else}
            <MemberToConfirm
              {member}
              onRefresh={handleRefreshMemberList}
              readOnly={!data.canEditMembers}
            />
          {/if}
        {/each}
      {/if}
      {#each sortedMembers(data.members) as member}
        <MemberStandard
          {member}
          onRefresh={handleRefreshMemberList}
          isMyself={member.user.email === $userInfo.email}
          isOnlyAdmin={member.user.email === $userInfo.email &&
            data.members.filter((m) => m.isAdmin).length === 1}
          readOnly={!data.canEditMembers}
        />
      {/each}
    </div>
  {/if}
</EnsureLoggedIn>
