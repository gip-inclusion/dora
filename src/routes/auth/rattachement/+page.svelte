<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import StructureSearch from "$lib/components/specialized/establishment-search/search.svelte";
  import { defaultAcceptHeader, getApiURL } from "$lib/utils/api";
  import {
    token,
    userInfo,
    validateCredsAndFillUserInfo,
  } from "$lib/utils/auth";
  import { trackJoinStructure } from "$lib/utils/plausible";
  import { get } from "svelte/store";
  import AuthLayout from "../auth-layout.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;

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
      }),
    });

    const result = {
      ok: response.ok,
      status: response.status,
    };

    if (response.ok) {
      result.data = await response.json();
      await validateCredsAndFillUserInfo();
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
      ctaLabel = "Adhérer à la structure";
    }
  }
</script>

<EnsureLoggedIn>
  <AuthLayout>
    <StructureSearch bind:establishment title="Identifiez votre structure">
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
                En cliquant sur <span class="italic"
                  >Adhérer à la structure</span
                >, je déclare faire partie de la structure mentionnée ci-dessus
                et j’atteste connaître les risques encourus en cas de faux et
                d’usage de faux.
              </div>
            {/if}
            <div class="mt-s24 flex justify-end">
              <Button
                label={ctaLabel}
                on:click={handleJoin}
                preventDefaultOnMouseDown
              />
            </div>
          </div>
        {/if}
      </div>
    </StructureSearch>
  </AuthLayout>
</EnsureLoggedIn>
