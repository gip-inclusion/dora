<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import MemberInvited from "./member-invited.svelte";
  import MemberStandard from "./member-standard.svelte";
  import MemberToConfirm from "./member-to-confirm.svelte";
  import ModalAddUser from "./modal-add-user.svelte";
  import { userAddIcon } from "$lib/icons";
  import { getMembers, getPutativeMembers } from "$lib/requests/structures";
  import { userInfo } from "$lib/utils/auth";
  import { structure } from "../store";
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
      <LinkButton
        label="Ajouter un collaborateur"
        icon={userAddIcon}
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
