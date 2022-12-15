<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
</script>

<div class="wrapper-container">
  <div class="wrapper">
    <div class="">
      <h4>Connaissez-vous monenfant.fr ?</h4>
      <p class="mt-s16 text-f14 leading-24 text-gray-text">
        Conçu par les Caf et la Cnaf, le portail « monenfant.fr » référence les
        structures d’accueil destinées aux jeunes enfants, les services
        existants pour informer et accompagner les parents de jeunes enfants
        mais également les assistants et assistantes maternelles actuellement en
        activité.
      </p>
    </div>
    <div class="shrink-0">
      <LinkButton label="Accéder au site" to="https://monenfant.fr/" otherTab />
    </div>
  </div>
</div>

<style lang="postcss">
  .wrapper-container {
    padding: 20px 20px 24px 24px;
    background-color: var(--col-white);
    border-radius: var(--s8);
    box-shadow: var(--shadow-sm);
  }

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
