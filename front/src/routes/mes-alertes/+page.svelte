<script lang="ts">
  import BookmarkLineBusiness from "svelte-remix/BookmarkLineBusiness.svelte";
  import ExternalLinkLineSystem from "svelte-remix/ExternalLinkLineSystem.svelte";

  import illustration from "$lib/assets/illustrations/illu-favoris.svg";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import type { SavedSearch } from "$lib/types";
  import { getApiURL } from "$lib/utils/api";
  import { refreshUserInfo, userInfo } from "$lib/utils/auth";
  import { fetchData } from "$lib/utils/misc";
  import { onMount } from "svelte";
  import SavedSearchCard from "./saved-search-card.svelte";
  import { URL_HELP_SITE } from "$lib/consts";

  let savedSearches: SavedSearch[] | undefined = $state();

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
    refreshUserInfo();
  }

  onMount(async () => {
    savedSearches = await getSavedSearches();
  });
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1 class="text-france-blue text-center">Mes alertes</h1>

    <div class="mb-s32">
      <Breadcrumb currentLocation="saved-searches" />
    </div>
    {#if savedSearches == null}
      <p class="mb-s40 text-f16 text-gray-dark">Chargement…</p>
    {:else if savedSearches.length}
      <p class="mb-s40 text-f21 text-gray-dark font-bold">
        {$userInfo.savedSearches.length} alerte{$userInfo.savedSearches.length >
        1
          ? "s"
          : ""}
      </p>
      <div class="gap-s16 flex flex-col">
        {#each savedSearches as search}
          <SavedSearchCard {search} onDelete={handleDelete} />
        {/each}
      </div>
    {:else}
      <div
        class="gap-s40 border-gray-03 px-s20 py-s32 flex flex-col-reverse items-center justify-center rounded-lg border lg:flex-row"
      >
        <div class="max-w-lg basis-1/2 text-center">
          <div class="mb-s12 h-s24 w-s24 mx-auto">
            <BookmarkLineBusiness />
          </div>
          <h2 class="legend text-f32 text-gray-text leading-40 font-bold">
            Vous n’avez pas encore créé d’alerte
          </h2>
          <p class="legend">
            Pour mettre en place votre première alerte, il vous suffit
            d’effectuer une recherche pour un lieu spécifique, ou pour un lieu
            et une thématique combinés. Une fois que vous êtes sur la page des
            résultats, il vous faudra simplement cliquer sur le bouton
            "Sauvegarder la recherche". Dès qu’un nouveau service répondant à
            ces critères est ajouté sur DORA, vous recevrez une notification par
            e-mail.
          </p>

          <a
            target="_blank"
            title="Ouverture dans une nouvelle fenêtre"
            rel="noopener"
            href={`${URL_HELP_SITE}/article/alertes-comment-enregistrer-des-recherches-1xpnlc9/?bust=1698336652095`}
            class="text-magenta-cta inline-block h-full"
          >
            Découvrez comment créer une alerte
            <span
              class="h-s20 w-s20 pl-s4 pt-s6 inline-block fill-current"
              aria-hidden="true"
            >
              <ExternalLinkLineSystem />
            </span>
          </a>
        </div>
        <div class="shrink-0">
          <img src={illustration} alt="" />
        </div>
      </div>
    {/if}
  </CenteredGrid>
</EnsureLoggedIn>
