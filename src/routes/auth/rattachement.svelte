<script>
  import { page } from "$app/stores";
  import { token, userInfo } from "$lib/auth";
  import { defaultAcceptHeader, getApiURL } from "$lib/utils/api.js";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import Button from "$lib/components/button.svelte";
  import AuthLayout from "./_auth_layout.svelte";
  import StructureSearch from "$lib/components/structures/search.svelte";
  import { get } from "svelte/store";
  import { goto } from "$app/navigation";

  let siret = $page.url.searchParams.get("siret");

  let establishment;
  let tabId;

  async function handleJoin() {
    plausible("inscription", { props: { step: "Adhésion structure" } });
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
    ?.map((s) => s.siret)
    ?.includes(establishment?.siret);
  $: alreadyRequested = $userInfo?.pendingStructures
    ?.map((s) => s.siret)
    ?.includes(establishment?.siret);
</script>

<svelte:head>
  <title>Rattachement à votre structure | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <AuthLayout>
    <StructureSearch {siret} bind:establishment bind:tabId blockPoleEmploi>
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
                label={alreadyRequested
                  ? "Relancer l’administrateur"
                  : alreadyMember
                  ? "Accéder à la structure"
                  : "Adhérer à la structure"}
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
