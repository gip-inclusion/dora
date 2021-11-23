<script context="module">
  export const ssr = false;
  import { getStructure, getMembers } from "$lib/structures";
  import { getMyStructures, getStructures } from "$lib/structures";
  import { isStaff } from "$lib/auth";

  export async function load({ page, _fetch, _session, _context }) {
    const structures = isStaff
      ? await getStructures()
      : await getMyStructures();
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
  import LinkButton from "$lib/components/link-button.svelte";

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
  <title>Ma structure | {structure.name} | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <AddUserModal
    bind:isOpen={addUserModalIsOpen}
    {structure}
    {members}
    onRefresh={handleRefreshMemberList}
  />
  <CenteredGrid --col-bg="var(--col-gray-00)" topPadded>
    <div class="col-start-1 col-span-full mb-s80">
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
            <div class="border border-gray-01 rounded px-s24 py-s16">
              <h4 class="text-gray-text ">{structure.name}</h4>
              <p class="text-gray-text-alt2 mt-s12">SIRET: {structure.siret}</p>
            </div>
            <div class="border border-gray-01 rounded px-s24 py-s16">
              <h5>Adresse</h5>
              <p class="text-gray-text-alt2">
                {structure.address1}<br />
                {#if structure.address2}{structure.address2}<br />{/if}
                {structure.postalCode}
                {structure.city}<br />
              </p>
              <h5 class="mt-s12">Contact</h5>
              <p class="text-gray-text-alt2">
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
              </p>
              <h5 class="mt-s12">Résumé</h5>
              <p class="text-gray-text-alt2">{structure.shortDesc}</p>
            </div>
            <div class="flex justify-end">
              <LinkButton
                label="Modifier les informations"
                to="/tableau-de-bord/structures/{structure.slug}/editer"
              />
            </div>
          </Fieldset>
        </div>
        <div class="flex-1">
          {#if members}
            <div class="mt-s48">
              <h3>Vos collaborateurs</h3>
              <div class="flex flex-col gap-s8 mt-s32 mb-s32">
                {#each sortedMembers(members) as member}
                  <Member
                    {member}
                    onRefresh={handleRefreshMemberList}
                    isMyself={member.user.email === $userInfo.email}
                    isOnlyAdmin={member.user.email === $userInfo.email &&
                      members.filter((m) => m.isAdmin).length === 1}
                  />
                {/each}
              </div>
              <div class="flex justify-end">
                <Button
                  label="Ajouter des collaborateurs"
                  secondary
                  on:click={() => (addUserModalIsOpen = true)}
                />
              </div>
            </div>
          {/if}
        </div>
      </div>
    </div>
  </CenteredGrid>
</EnsureLoggedIn>
