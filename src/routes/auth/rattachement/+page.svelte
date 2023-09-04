<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import StructureSearch from "$lib/components/specialized/establishment-search/search.svelte";
  import { defaultAcceptHeader, getApiURL } from "$lib/utils/api";
  import { token, userInfo, refreshUserInfo } from "$lib/utils/auth";
  import { trackJoinStructure } from "$lib/utils/plausible";
  import { get } from "svelte/store";
  import AuthLayout from "../auth-layout.svelte";
  import type { PageData } from "./$types";
  import { CGU_VERSION } from "../../(static)/cgu/version";
  import loopImg from "$lib/assets/icons/loop.svg";

  export let data: PageData;

  let cguAccepted = false;
  let { establishment } = data;
  let ctaLabel = "";

  async function handleJoin() {
    trackJoinStructure();

    const targetUrl = `${getApiURL()}/auth/join-structure/`;
    const response = await fetch(targetUrl, {
      method: "POST",
      headers: {
        Accept: defaultAcceptHeader,
        "Content-Type": "application/json",
        Authorization: `Token ${get(token)}`,
      },
      body: JSON.stringify({
        siret: establishment.siret,
        cguVersion: CGU_VERSION,
      }),
    });

    const result = {
      ok: response.ok,
      status: response.status,
    };

    if (response.ok) {
      result.data = await response.json();

      await refreshUserInfo();
      await goto(`/structures/${result.data.slug}`);
    } else {
      try {
        result.error = await response.json();
      } catch (err) {
        console.error(err);
      }
    }
    return result;
  }

  $: alreadyMember = $userInfo?.structures
    ?.map((struct) => struct.siret)
    ?.includes(establishment?.siret);
  $: alreadyRequested = $userInfo?.pendingStructures
    ?.map((struct) => struct.siret)
    ?.includes(establishment?.siret);

  $: {
    if (alreadyRequested) {
      ctaLabel = "Relancer l’administrateur";
    } else if (alreadyMember) {
      ctaLabel = "Accéder à la structure";
    } else {
      ctaLabel = "Rejoindre la structure";
    }
  }
</script>

<EnsureLoggedIn>
  <AuthLayout>
    <StructureSearch
      bind:establishment
      title="Retrouvez votre structure"
      description="Pour accéder à toutes les fonctionnalités, merci de nous indiquer la structure dans laquelle vous travaillez :"
    >
      <div slot="cta">
        {#if establishment?.siret}
          <div class="mt-s24">
            {#if alreadyMember}
              Votre compte est déjà rattaché à cette structure.
            {:else if alreadyRequested}
              Votre précédente demande d’adhésion est en attente de validation
              par l’administrateur de la structure.
            {:else}
              <div class="legend">
                <label class="flex flex-row items-start">
                  <input
                    bind:checked={cguAccepted}
                    type="checkbox"
                    class="hidden "
                  />
                  <div
                    class="flex h-s24 w-s24 shrink-0 justify-center rounded border border-gray-03"
                  >
                    <div
                      class=" h-s12 w-s12 self-center bg-magenta-cta"
                      class:hidden={!cguAccepted}
                    />
                  </div>
                  <span class="ml-s16 inline-block  text-f14 text-gray-text">
                    Je déclare avoir lu les
                    <a
                      href="/cgu"
                      class="underline"
                      target="_blank"
                      rel="noopener">Conditions générales d’utilisation</a
                    > et faire partie de la structure mentionnée ci-dessus.</span
                  >
                </label>
              </div>
            {/if}
            <div class="mt-s24 flex justify-end">
              <Button
                type="submit"
                label={ctaLabel}
                on:click={handleJoin}
                preventDefaultOnMouseDown
                disabled={!cguAccepted}
              />
            </div>
          </div>
        {/if}
      </div>
    </StructureSearch>

    <div class="mt-s24 rounded-md border border-gray-02 bg-white px-s32 py-s24">
      <a
        href="https://aide.dora.inclusion.beta.gouv.fr/fr/article/comment-sinscrire-sur-dora-14d64n0/#3-03-adherer-a-votre-structure"
        target="_blank"
        rel="noopener"
        class="flex items-center"
        title="Ouverture dans une nouvelle fenêtre"
      >
        <img src={loopImg} alt="" class="mr-s20" />
        <span class="text-f18 font-bold text-france-blue hover:underline">
          Besoin d’aide ?
        </span>
      </a>
    </div>
  </AuthLayout>
</EnsureLoggedIn>
