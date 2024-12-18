<script lang="ts">
  import { onMount } from "svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { arrowLeftLineIcon, flashLightIcon } from "$lib/icons";
  import Layout from "../orientation-layout.svelte";
  import type { PageData } from "./$types";
  import { orientation } from "../store";
  import illustration from "$lib/assets/illustrations/illu-favs-moderation.svg";
  import Notice from "$lib/components/display/notice.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { URL_DOCUMENTATION_ORIENTATION } from "$lib/consts";

  export let data: PageData;

  const showContactBeneficiary = !$orientation.beneficiaryEmail;
  onMount(() => {
    window._mtm = window._mtm || [];
    window._mtm.push({ event: "orienter/merci" });
  });
</script>

<EnsureLoggedIn>
  <Layout {data}>
    <div
      class="gap-s46 px-s14 mt-s56 flex flex-col-reverse items-start justify-around rounded-md border border-gray-03 py-s32 lg:flex-row"
    >
      <div class="max-w-lg basis-1/2 text-center">
        <div class="mx-auto mb-s12 h-s24 w-s24 text-orange">
          {@html flashLightIcon}
        </div>
        <h2 class="font-bold text-orange">
          Votre demande fera l’objet d’une vérification par nos équipes.
        </h2>
        <p class="legend">
          Notre système sélectionne certaines orientations pour modération,
          notamment si vous êtes nouvellement inscrit·e ou si des possibles
          anomalies sont détectées.
        </p>
        <p class="legend">
          Pas d’inquiétude, nos équipes vérifieront cela rapidement et vous
          tiendront informé·e. Si l’orientation est validée, vous recevrez une
          confirmation et elle sera transmise à la structure porteuse du service
          “XXX”.
        </p>
        <p class="legend">
          Sinon, une réponse vous sera envoyée pour justifier le choix.
        </p>
        <p class="legend">
          Consulter notre <a
            class="text-magenta-cta underline"
            target="_blank"
            href={URL_DOCUMENTATION_ORIENTATION}>documentation</a
          > pour en savoir plus.
        </p>

        {#if showContactBeneficiary}
          <div class="mb-s28">
            <Notice type="info" title="Pensez à informer le ou la bénéficiaire">
              <p class="text-left text-f14 text-gray-text">
                Conformément aux préférences de contact du ou de la
                bénéficiaire, veuillez prendre contact avec lui ou elle pour
                l’informer qu’une prescription a été réalisée en son nom.
              </p>
            </Notice>
          </div>
        {/if}

        <LinkButton
          icon={arrowLeftLineIcon}
          label="Retour à la fiche"
          to="/services/{data.isDI ? 'di--' : ''}{data.service.slug}"
          noBackground
        />
      </div>
      <div class="mt-s36 flex-shrink-0 fill-orange">
        <img
          src={illustration}
          alt="Personne avec un sac à dos feuilletant des notes"
        />
      </div>
    </div>
  </Layout>
</EnsureLoggedIn>
