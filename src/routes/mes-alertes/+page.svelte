<script lang="ts">
  import illustration from "$lib/assets/illustrations/illu-favoris.svg";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { externalLinkIcon, starSmileLineIcon } from "$lib/icons";
  import type { SavedSearch } from "$lib/types";
  import { getApiURL } from "$lib/utils/api";
  import { userInfo } from "$lib/utils/auth";
  import { fetchData } from "$lib/utils/misc";
  import { onMount } from "svelte";
  import SavedSearchCard from "./saved-search-card.svelte";

  let savedSearches: SavedSearch[] | undefined = undefined;

  async function getSavedSearches() {
    const url = `${getApiURL()}/saved-searches/`;
    const result = await fetchData(url);
    if (result.ok) {
      return result.data as Array<SavedSearch>;
    }
    return [];
  }

  function handleDelete(searchId: number) {
    savedSearches = savedSearches?.filter((search) => search.id !== searchId);
  }

  onMount(async () => {
    savedSearches = await getSavedSearches();
  });
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1 class="text-center text-france-blue">Mes alertes</h1>

    <div class="mb-s32">
      <Breadcrumb currentLocation="saved-searches" dark />
    </div>
    {#if savedSearches == null}
      <p class="mb-s40 text-f16 text-gray-dark">Chargement…</p>
    {:else if savedSearches.length}
      <p class="mb-s40 text-f21 font-bold text-gray-dark">
        {$userInfo.savedSearches.length} alerte{$userInfo.savedSearches.length >
        1
          ? "s"
          : ""}
      </p>
      <div class="flex flex-col gap-s16">
        {#each savedSearches as search}
          <SavedSearchCard {search} onDelete={handleDelete} />
        {/each}
      </div>
    {:else}
      <div
        class="flex flex-col-reverse items-center justify-center gap-s40 rounded-md border border-gray-03 px-s20 py-s32 lg:flex-row"
      >
        <div class="max-w-lg basis-1/2 text-center">
          <div class="mx-auto mb-s12 h-s24 w-s24">
            {@html starSmileLineIcon}
          </div>
          <h2 class="legend text-f32 font-bold leading-40 text-gray-text">
            Vous n’avez pas encore créé d’alerte
          </h2>
          <p class="legend">
            Pour mettre en place votre première alerte, il vous suffit
            d‘effectuer une recherche pour un lieu spécifique, ou pour un lieu
            et une thématique combinés. Une fois que vous êtes sur la page des
            résultats, il vous faudra simplement cliquer sur le bouton
            "Sauvegarder la recherche". Dès qu‘un nouveau service répondant à
            ces critères est ajouté sur DORA, vous recevrez une notification par
            e-mail.
          </p>

          <a
            target="_blank"
            title="Ouverture dans une nouvelle fenêtre"
            rel="noopener"
            href="https://aide.dora.inclusion.beta.gouv.fr/fr/article/alertes-comment-enregistrer-des-recherches-1xpnlc9/?bust=1698336652095"
            class="inline-block h-full text-magenta-cta"
          >
            Découvrez comment créer une alerte
            <span
              class="inline-block h-s20 w-s20 fill-current pl-s4 pt-s6"
              aria-hidden
            >
              {@html externalLinkIcon}
            </span>
          </a>
        </div>
        <div class="flex-shrink-0">
          <img src={illustration} alt="" />
        </div>
      </div>
    {/if}
  </CenteredGrid>
</EnsureLoggedIn>
