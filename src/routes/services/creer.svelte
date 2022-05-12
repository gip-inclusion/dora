<script context="module">
  import { get } from "svelte/store";
  import { userInfo } from "$lib/auth";

  import { getLastDraft, getServicesOptions } from "$lib/services";
  import { getStructures } from "$lib/structures";

  export async function load() {
    const user = get(userInfo);
    let structures = [];

    if (user?.isStaff) {
      structures = await getStructures();
    } else if (user) {
      structures = user.structures;
    }

    return {
      props: {
        lastDraft: await getLastDraft(),
        servicesOptions: await getServicesOptions(),
        structures,
      },
    };
  }
</script>

<script>
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";

  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import Notice from "$lib/components/notice.svelte";
  import Button from "$lib/components/button.svelte";

  import { getNewService } from "./_form/_stores.js";
  import ServiceFormWrapper from "./_form/_service-form-wrapper.svelte";
  import Card from "$lib/components/structures/card.svelte";

  export let servicesOptions, structures, lastDraft;

  let service = getNewService();

  if (structures.length === 1) {
    service.structure = structures[0].slug;
    service.structureInfo = structures[0];
  } else {
    // si la structure est renseignée dans l'URL, force celle-là
    const structureSlug = $page.url.searchParams.get("structure");
    if (structureSlug) {
      const structure = structures.find((s) => s.slug === structureSlug);
      service.structure = structureSlug;
      service.structureInfo = structure;
    }
  }
  if (service.structure && lastDraft?.structure !== service.structure) {
    lastDraft = null;
  }

  function handleOpenLastDraft() {
    goto(`/services/${lastDraft.slug}/editer`);
  }
</script>

<svelte:head>
  <title>Référencer votre service | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid>
    <div class="col-span-full pt-s48 pb-s24">
      <div class="flex flex-wrap justify-between">
        <div class="w-2/3"><h1>Création du service</h1></div>
        {#if service.structureInfo}
          <div class="w-1/3"><Card structure={service.structureInfo} /></div>
        {/if}
      </div>

      {#if !structures.length}
        <Notice title="Impossible de créer un nouveau service" type="error">
          <p class="text-f14">
            Vous n’êtes rattaché à aucune structure.
          </p></Notice
        >
      {:else if lastDraft}
        <Notice
          title="Vous n’avez pas finalisé votre précédente saisie"
          hasCloseButton
        >
          <p class="text-f14">
            Souhaitez-vous continuer la saisie du service ?
          </p>

          <Button
            on:click={handleOpenLastDraft}
            slot="button"
            small
            secondary
            label="Reprendre"
          />
        </Notice>
      {/if}
    </div>
  </CenteredGrid>
  {#if structures.length}
    <ServiceFormWrapper bind:service bind:servicesOptions {structures} />
  {/if}
</EnsureLoggedIn>
