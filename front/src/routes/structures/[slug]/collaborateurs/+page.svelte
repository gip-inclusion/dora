<script lang="ts">
  import UserAddLineUserFaces from "svelte-remix/UserAddLineUserFaces.svelte";

  import Button from "$lib/components/display/button.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { getMembers, getPutativeMembers } from "$lib/requests/structures";
  import { userInfo } from "$lib/utils/auth";

  import { structure } from "../store";
  import MemberInvited from "./member-invited.svelte";
  import MemberStandard from "./member-standard.svelte";
  import MemberToConfirm from "./member-to-confirm.svelte";
  import ModalAddUser from "./modal-add-user.svelte";
  import type { PageData } from "./$types";
  import NoMemberNotice from "./no-member-notice.svelte";
  import { hasAtLeastTwoMembersOrInvitedMembers } from "../quick-start";

  interface Props {
    data: PageData;
  }

  let { data: initialData }: Props = $props();
  let data = $state(initialData);

  let modalAddUserIsOpen = $state(false);

  let showNoMemberNotice = $derived(
    !hasAtLeastTwoMembersOrInvitedMembers(data.members, data.putativeMembers)
  );

  async function handleRefreshMemberList() {
    const [members, putativeMembers] = await Promise.all([
      getMembers($structure.slug),
      getPutativeMembers($structure.slug),
    ]);
    data.members = members ?? undefined;
    data.putativeMembers = putativeMembers ?? undefined;
  }

  function sortMembers(items) {
    return [...items].sort((a, b) => {
      if (a.isAdmin && !b.isAdmin) {
        return -1;
      }
      if (!a.isAdmin && b.isAdmin) {
        return 1;
      }
      const nameA = a.user.lastName || a.user.email;
      const nameB = b.user.lastName || b.user.email;
      return nameA.localeCompare(nameB, "fr");
    });
  }

  let sortedMembersList = $derived(
    data.members ? sortMembers(data.members) : []
  );
  let sortedPutativeMembersList = $derived(
    data.putativeMembers ? sortMembers(data.putativeMembers) : []
  );

  let canAdd = $derived($structure.canEditMembers);
</script>

<EnsureLoggedIn>
  {#if canAdd}
    <ModalAddUser
      bind:isOpen={modalAddUserIsOpen}
      structure={$structure}
      members={data.members}
      onRefresh={handleRefreshMemberList}
      suggestAdmin={!$structure.hasAdmin}
    />
  {/if}

  <div class="mb-s24 md:flex md:items-center md:justify-between">
    <h2 class="text-france-blue">Collaborateurs</h2>
    {#if canAdd}
      <Button
        label="Ajouter un collaborateur"
        icon={UserAddLineUserFaces}
        onclick={() => (modalAddUserIsOpen = true)}
      />
    {/if}
  </div>

  {#if $structure.canViewMembers}
    {#if $structure.isMember && $structure.canEditMembers && showNoMemberNotice}
      <div class="mb-s24 gap-s8 flex flex-col">
        <NoMemberNotice />
      </div>
    {/if}

    <div class="mb-s32 mt-s32 gap-s8 flex flex-col">
      {#if canAdd && data.putativeMembers}
        {#each sortedPutativeMembersList as member}
          {#if member.invitedByAdmin}
            <MemberInvited
              {member}
              onRefresh={handleRefreshMemberList}
              readOnly={!($structure.canEditMembers || canAdd)}
            />
          {:else}
            <MemberToConfirm
              {member}
              onRefresh={handleRefreshMemberList}
              readOnly={!$structure.canEditMembers}
            />
          {/if}
        {/each}
      {/if}
      {#each sortedMembersList as member}
        <MemberStandard
          {member}
          structureSlug={data.structure.slug}
          onRefresh={handleRefreshMemberList}
          isMyself={member.user.email === $userInfo?.email}
          readOnly={!$structure.canEditMembers}
        />
      {/each}
    </div>
  {/if}
</EnsureLoggedIn>
