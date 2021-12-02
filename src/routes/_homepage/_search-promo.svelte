<script>
  import LinkButton from "$lib/components/link-button.svelte";

  import SearchResultWrapper from "./_search_result_wrapper.svelte";
</script>

<style lang="postcss">
  .wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--s24);
  }

  h4 {
    color: var(--col-info);
  }

  @screen lg {
    .wrapper {
      flex-direction: row;
    }
  }
</style>

<SearchResultWrapper>
  <div class="wrapper">
    <div class="">
      <h4>Connaissez-vous monenfant.fr ?</h4>
      <p class="mt-s16 text-gray-text text-f14 leading-24">
        Conçu par les Caf et la Cnaf, le portail « monenfant.fr » référence les
        structures d’accueil destinées aux jeunes enfants, les services
        existants pour informer et accompagner les parents de jeunes enfants
        mais également les assistants et assistantes maternelles actuellement en
        activité.
      </p>
    </div>
    <div class="flex-shrink-0">
      <LinkButton
        type="button"
        label="Accéder au site"
        to="https://monenfant.fr/"
        otherTab
      />
    </div>
  </div>
</SearchResultWrapper>
