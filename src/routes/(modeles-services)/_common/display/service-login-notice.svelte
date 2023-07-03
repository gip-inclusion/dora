<script lang="ts">
  import { page } from "$app/stores";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import AbTestingSection from "$lib/components/specialized/ab-testing-section.svelte";
  import { getAbTestingUserGroup } from "$lib/utils/ab-testing";
  import { trackMobilisationLogin } from "$lib/utils/plausible";

  export let service;

  function trackClick() {
    trackMobilisationLogin(service);
  }
</script>

<AbTestingSection
  abTestingName="mobilisation"
  showIfGroups={["mobilisation--ancien-design"]}
>
  <div class="flex w-full flex-col rounded-lg bg-info-light p-s16">
    <strong class="mb-s8 text-f17 text-service-blue-info">
      Pour mobiliser ce service, vous devez vous connecter&nbsp;!
    </strong>
    <div class="mb-s24 text-f14 text-gray-text">
      En vous connectant, vous aurez accès aux informations de contact afin de
      mobiliser ce service pour votre bénéficiaire.
    </div>

    <div>
      <LinkButton
        on:click={trackClick}
        small
        label="Se connecter"
        to={`/auth/connexion?next=${encodeURIComponent($page.url.pathname)}`}
      />
    </div>
  </div>
</AbTestingSection>

<AbTestingSection
  abTestingName="mobilisation"
  showIfGroups={["mobilisation--fond-bleu", "mobilisation--fond-blanc"]}
>
  {@const blueDesign =
    getAbTestingUserGroup("mobilisation") === "mobilisation--fond-bleu"}

  <div class="mb-s24 text-f14 text-gray-text" class:text-white={blueDesign}>
    Pour accéder aux informations de contact de ce service, vous devez vous
    connecter.
  </div>

  <div>
    <LinkButton
      on:click={trackClick}
      extraClass={blueDesign
        ? "bg-white !text-france-blue hover:!text-white"
        : ""}
      label="S‘identifier avec Inclusion Connect"
      to={`/auth/connexion?next=${encodeURIComponent($page.url.pathname)}`}
    />
  </div>
</AbTestingSection>
