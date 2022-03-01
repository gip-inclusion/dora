<script context="module">
  import { get } from "svelte/store";
  import {
    getStructure,
    getMembers,
    getPutativeMembers,
    getMyStructures,
  } from "$lib/structures";
  import { userInfo } from "$lib/auth";

  export async function load({ params }) {
    const info = get(userInfo);
    const structureSlug = params.slug;

    const myStructures = await getMyStructures();
    const canSeeStructure = myStructures.find((s) => (s.slug = structureSlug));

    const structMembers = await getMembers(structureSlug);
    const userIsAdminOfStruct = structMembers?.find(
      (m) => m.user.email === info.email && m.isAdmin
    );
    if (canSeeStructure || info?.isBizdev || info?.isStaff) {
      const canSeeMembers =
        userIsAdminOfStruct || info?.isBizdev || info?.isStaff;
      return {
        props: {
          structure: await getStructure(structureSlug),
          members: structMembers,
          putativeMembers: canSeeMembers
            ? await getPutativeMembers(structureSlug)
            : [],
          canEditStructure: userIsAdminOfStruct || info?.isStaff,
          canSeeMembers,
          canEditMembers: userIsAdminOfStruct || info?.isStaff,
        },
      };
    }
    return {};
  }
</script>

<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import MemberInvited from "./_member_invited.svelte";
  import MemberToConfirm from "./_member_to_confirm.svelte";
  import Button from "$lib/components/button.svelte";
  import AddUserModal from "./_add-user-modal.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import MemberStandard from "./_member_standard.svelte";

  export let structure, members, putativeMembers;
  export let canEditStructure, canSeeMembers, canEditMembers;
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
  <title>Ma structure | {structure?.name} | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  {#if structure}
    <AddUserModal
      bind:isOpen={addUserModalIsOpen}
      {structure}
      {members}
      onRefresh={handleRefreshMemberList}
    />
    <CenteredGrid --col-bg="var(--col-gray-00)" topPadded>
      <div class="col-span-full col-start-1 mb-s80">
        <div class="mb-s32">
          <h2>Ma structure</h2>
        </div>
        <div class="border-t border-gray-03" />
        <div class="flex gap-s24">
          <div class="flex-1">
            <Fieldset
              title="Présentation de ma structure"
              description="Vous trouvez ici les informations concernant votre structure, tels qu’ils sont visibles sur le site DORA."
            >
              <div class="rounded border border-gray-01 px-s24 py-s16">
                <h4 class="text-gray-text">{structure.name}</h4>
                <div class="legend mt-s12">Siret : {structure.siret}</div>
              </div>
              <div class="rounded border border-gray-01 px-s24 py-s16">
                <h5>Adresse</h5>
                <div class="legend">
                  {structure.address1}<br />
                  {#if structure.address2}{structure.address2}<br />{/if}
                  {structure.postalCode}
                  {structure.city}<br />
                </div>
                <h5 class="mt-s12">Contact</h5>
                <div class="legend">
                  {#if structure.phone}
                    <a class="underline" href="tel:{structure.phone}">
                      {structure.phone}
                    </a>
                    <br />
                  {/if}
                  {#if structure.email}
                    <a class="underline" href="mailto:{structure.email}">
                      {structure.email}
                    </a>
                    <br />
                  {/if}
                  {#if structure.url}
                    <a
                      class="underline"
                      target="_blank"
                      rel="noopener nofollow"
                      href={structure.url}
                    >
                      {structure.url}
                    </a>
                  {/if}
                </div>
                <h5 class="mt-s12">Résumé</h5>
                <div class="legend">{structure.shortDesc}</div>
              </div>
              {#if !canEditStructure}
                <div class="flex justify-end">
                  <LinkButton
                    label="Modifier les informations"
                    to="/tableau-de-bord/structures/{structure.slug}/editer"
                  />
                </div>
              {/if}
            </Fieldset>
          </div>
          <div class="flex-1">
            {#if canSeeMembers && members}
              <div class="mt-s48">
                <h3>Vos collaborateurs</h3>
                <div class="mt-s32 mb-s32 flex flex-col gap-s8">
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
                {#if !canEditMembers}
                  <div class="flex justify-end">
                    <Button
                      label="Ajouter des collaborateurs"
                      secondary
                      on:click={() => (addUserModalIsOpen = true)}
                    />
                  </div>
                {/if}
              </div>
            {/if}
          </div>
        </div>
      </div>
    </CenteredGrid>
  {:else}
    <CenteredGrid --col-bg="var(--col-gray-00)" topPadded>
      <div class="col-span-full col-start-1 mb-s80">
        Vous ne faites pas partie de cette structure
      </div>
    </CenteredGrid>
  {/if}
</EnsureLoggedIn>
