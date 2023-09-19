<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { arrowLeftLineIcon, flashLightIcon } from "$lib/icons";
  import Layout from "../orientation-layout.svelte";
  import type { PageData } from "./$types";
  import { initEmptyOrientation, orientation } from "../store";
  import illustration from "$lib/assets/illustrations/illu-favs.svg";
  import Notice from "$lib/components/display/notice.svelte";

  export let data: PageData;

  const showContactBeneficiary = !$orientation.beneficiaryEmail;
  $orientation = initEmptyOrientation();
</script>

<Layout {data}>
  <div
    class="gap-s46 px-s14 mt-s56 flex flex-col-reverse items-center justify-around rounded-md border border-gray-03 py-s32 lg:flex-row"
  >
    <div class="max-w-lg basis-1/2 text-center">
      <div class="mx-auto mb-s12 h-s24 w-s24">
        {@html flashLightIcon}
      </div>
      <h2 class=" font-bold text-gray-text">
        Votre demande a été transmise à la structure porteuse du service
      </h2>
      <p class="legend">
        Vous allez recevoir une copie de cette demande par e-mail, dans quelques
        instants.
        {#if $orientation.beneficiaryContactPreferences.includes("EMAIL")}
          <br />Le ou la bénéficiaire recevra également une notice
          d’information.
        {/if}
      </p>

      {#if showContactBeneficiary}
        <div class="mb-s28">
          <Notice type="info" title="Pensez à informer le ou la bénéficiaire">
            <p class="text-left text-f14 text-gray-text">
              Conformément aux préférences de contact du ou de la bénéficiaire,
              veuillez prendre contact avec lui ou elle pour l’informer qu’une
              prescription a été réalisée en son nom.
            </p>
          </Notice>
        </div>
      {/if}

      <LinkButton
        icon={arrowLeftLineIcon}
        label="Retour à la fiche"
        to="/services/{data.service.slug}"
        noBackground
      />
    </div>
    <div class="flex-shrink-0">
      <img
        src={illustration}
        alt="Personne avec un sac à dos feuilletant des notes"
      />
    </div>
  </div>
</Layout>
