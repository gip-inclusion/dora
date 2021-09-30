<script>
  import LinkButton from "$lib/components/link-button.svelte";

  import SearchResultWrapper from "./_search_result_wrapper.svelte";
</script>

<style>
  .wrapper {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--s24);
  }

  h4 {
    color: var(--col-info);
  }

  p {
    margin-top: var(--s16);
    color: var(--col-text);
    font-size: var(--f14);
    line-height: var(--f24);
  }
</style>

<SearchResultWrapper>
  <div class="wrapper">
    <div class="">
      <h4>Connaissez-vous monenfant.fr ?</h4>
      <p>
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
        otherTab />
    </div>
  </div>
</SearchResultWrapper>
