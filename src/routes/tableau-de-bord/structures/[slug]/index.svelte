<script context="module">
  export const ssr = false;
  import { getStructure, getMembers } from "$lib/structures";
  import { getMyStructures } from "$lib/structures";

  export async function load({ page, _fetch, _session, _context }) {
    const structures = await getMyStructures();
    const structureSlug = page.params.slug;
    const structure = structures.find((s) => (s.slug = structureSlug));
    if (structure) {
      return {
        props: {
          structure: await getStructure(structureSlug),
          members: await getMembers(structureSlug),
        },
      };
    }
    return null;
  }
</script>

<script>
  import { userInfo } from "$lib/auth";

  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Member from "./_member.svelte";
  import Button from "$lib/components/button.svelte";
  import AddUserModal from "./_add-user-modal.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";

  export let structure, members;

  let addUserModalIsOpen = false;

  async function handleRefreshMemberList() {
    members = await getMembers(structure.slug);
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
  <title>Dora: Ma structure</title>
</svelte:head>

<EnsureLoggedIn>
  <AddUserModal
    bind:isOpen={addUserModalIsOpen}
    {structure}
    {members}
    onRefresh={handleRefreshMemberList} />
  <CenteredGrid --col-bg="var(--col-gray-00)">
    <div class="col-start-1 col-span-full mb-10">
      <div class="mb-4">
        <h2>Ma structure</h2>
      </div>
      <div class="border-t border-gray-03" />
      <div class="flex gap-3">
        <div class="flex-1">
          <Fieldset
            title="Présentation de ma structure"
            description="Vous trouvez ici les informations concernant votre structure, tels qu’ils sont visibles sur le site DORA.">
            <h4>{structure.name}</h4>
            <p class="text-gray-text-alt">SIRET: {structure.siret}</p>
          </Fieldset>
        </div>
        <div class="flex-1">
          {#if members}
            <div class="mt-6">
              <h3>Vos collaborateurs</h3>
              <div class="flex flex-col gap-1 mt-4 mb-4">
                {#each sortedMembers(members) as member}
                  <Member
                    {member}
                    onRefresh={handleRefreshMemberList}
                    isMyself={member.user.email === $userInfo.email} />
                {/each}
              </div>
              <div class="flex justify-end">
                <Button
                  label="Ajouter des collaborateurs"
                  secondary
                  on:click={() => (addUserModalIsOpen = true)} />
              </div>
            </div>
          {/if}
        </div>
      </div>
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
