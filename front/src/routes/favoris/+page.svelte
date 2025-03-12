<script lang="ts">
  import illustration from "$lib/assets/illustrations/illu-favs.svg";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { starSmileLineIcon } from "$lib/icons";
  import { userInfo } from "$lib/utils/auth";
  import type { PageData } from "./$types";
  import BookmarkCard from "./bookmark-card.svelte";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";

  export let data: PageData;

  const bookmarks = data.bookmarks || [];
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1 class="text-france-blue text-center">Mes favoris</h1>

    <div class="mb-s32">
      <Breadcrumb currentLocation="bookmarks" />
    </div>

    {#if bookmarks.length}
      <p class="mb-s40 text-f21 text-gray-dark font-bold">
        {$userInfo.bookmarks.length} favori{$userInfo.bookmarks.length > 1
          ? "s"
          : ""}
      </p>
      <div class="gap-s16 flex flex-col">
        {#each bookmarks as bookmark}
          <BookmarkCard {bookmark} />
        {/each}
      </div>
    {:else}
      <div
        class="gap-s40 px-s20 flex flex-col-reverse items-center justify-center lg:flex-row"
      >
        <div class="max-w-lg basis-1/2 text-center">
          <div class="mb-s12 h-s24 w-s24 mx-auto">
            {@html starSmileLineIcon}
          </div>
          <p class="legend text-gray-text font-bold">
            Vous n’avez pas encore ajouté de services à vos favoris.
          </p>
          <p class="legend">
            Pour ajouter votre premier service en favori, rien de plus
            simple&nbsp;: cliquez sur l’icône étoile et retrouvez-le dès que
            vous en aurez besoin, dans votre liste de favoris&nbsp;!
          </p>
        </div>
        <div class="shrink-0">
          <img
            src={illustration}
            alt="Personne avec un sac à dos feuilletant des notes"
          />
        </div>
      </div>
    {/if}
  </CenteredGrid>
</EnsureLoggedIn>
