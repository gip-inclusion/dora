<script lang="ts">
  import { onMount } from "svelte";
  import { userInfo } from "$lib/auth";
  import { starSmileLineIcon } from "$lib/icons";
  import illustration from "$lib/assets/ill-favs.svg";

  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import BookmarkCard from "./_bookmark-card.svelte";
  import type { Bookmark } from "$lib/types";

  let bookmarks: Bookmark[] = [];

  onMount(() => {
    // On ne veut pas être réactifs ici, afin que la liste ne soit pas rafraichie tant qu'on reste sur la page
    // sans quoi les favoris disparaitraient au clic, et on ne pourrait pas les reselectionner
    bookmarks = $userInfo?.bookmarks;
  });
</script>

<svelte:head>
  <title>Mes favoris | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1 class="mb-s64 text-center text-france-blue">Mes favoris</h1>
    {#if bookmarks.length}
      <p class="mb-s40 text-f21 font-bold text-gray-dark">
        {$userInfo.bookmarks.length} favori{$userInfo.bookmarks.length > 1
          ? "s"
          : ""}
      </p>
      <div class="flex flex-col gap-s16">
        {#each bookmarks as bookmark}
          <BookmarkCard {bookmark} />
        {/each}
      </div>
    {:else}
      <div
        class="flex flex-col-reverse items-center justify-center gap-s40 px-s20 lg:flex-row"
      >
        <div class="max-w-lg basis-1/2 text-center">
          <div class="mx-auto mb-s12 h-s24 w-s24">
            {@html starSmileLineIcon}
          </div>
          <p class="legend font-bold text-gray-text">
            Vous n’avez pas encore ajouté de services à vos favoris.
          </p>
          <p class="legend ">
            Pour ajouter votre premier service en favori, rien de plus
            simple&nbsp;: cliquez sur l’icône étoile et retrouvez-le dès que
            vous en aurez besoin, dans votre liste de favoris&nbsp;!
          </p>
        </div>
        <div class="flex-shrink-0">
          <img
            src={illustration}
            alt="Personne avec un sac à dos feuilletant des notes"
          />
        </div>
      </div>
    {/if}
  </CenteredGrid>
</EnsureLoggedIn>
