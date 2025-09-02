<script lang="ts">
  import { onMount } from "svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import ArrowLeftSLineArrows from "svelte-remix/ArrowLeftSLineArrows.svelte";
  import FlashlightLineWeather from "svelte-remix/FlashlightLineWeather.svelte";
  import Layout from "../orientation-layout.svelte";
  import type { PageData } from "./$types";
  import { initEmptyOrientation, orientation } from "../store";
  import illustration from "$lib/assets/illustrations/illu-favs.svg";
  import Notice from "$lib/components/display/notice.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  const showContactBeneficiary = !$orientation.beneficiaryEmail;
  $orientation = initEmptyOrientation();
  onMount(() => {
    window._mtm = window._mtm || [];
    window._mtm.push({ event: "orienter/merci" });
  });
</script>

<EnsureLoggedIn>
  <Layout {data}>
    <div
      class="gap-s46 px-s14 mt-s56 border-gray-03 py-s32 flex flex-col-reverse items-start justify-around rounded-lg border lg:flex-row"
    >
      <div class="max-w-lg basis-1/2 text-center">
        <div class="mb-s12 h-s24 w-s24 text-gray-text mx-auto fill-current">
          <FlashlightLineWeather />
        </div>
        <h2 class="text-gray-text font-bold">
          Votre demande a été transmise à la structure porteuse du service
        </h2>
        <p class="legend">
          Vous allez recevoir une copie de cette demande par e-mail, dans
          quelques instants.
          {#if $orientation.beneficiaryContactPreferences.includes("EMAIL")}
            <br />Le ou la bénéficiaire recevra également une notice
            d’information.
          {/if}
        </p>

        {#if showContactBeneficiary}
          <div class="mb-s28">
            <Notice type="info" title="Pensez à informer le ou la bénéficiaire">
              <p class="text-f14 text-gray-text text-left">
                Conformément aux préférences de contact du ou de la
                bénéficiaire, veuillez prendre contact avec lui ou elle pour
                l’informer qu’une prescription a été réalisée en son nom.
              </p>
            </Notice>
          </div>
        {/if}

        <LinkButton
          icon={ArrowLeftSLineArrows}
          label="Retour à la fiche"
          to="/services/{data.isDI ? 'di--' : ''}{data.service.slug}"
          noBackground
        />
      </div>
      <div class="mt-s36 shrink-0">
        <img
          src={illustration}
          alt="Personne avec un sac à dos feuilletant des notes"
        />
      </div>
    </div>
  </Layout>
</EnsureLoggedIn>
