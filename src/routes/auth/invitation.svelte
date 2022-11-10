<script context="module">
  import { getStructure } from "$lib/structures";

  export async function load({ url }) {
    const structure = await getStructure(url.searchParams.get("structure"));
    let parent = null;
    if (!structure) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    if (structure.parent) {
      parent = await getStructure(structure.parent);
    }

    return {
      props: { structure, parent },
    };
  }
</script>

<script>
  import { token, validateCredsAndFillUserInfo } from "$lib/auth";
  import { trackJoinStructure } from "$lib/utils/plausible";

  import { defaultAcceptHeader, getApiURL } from "$lib/utils/api.js";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import Button from "$lib/components/button.svelte";
  import AuthLayout from "./_auth_layout.svelte";
  import { get } from "svelte/store";
  import { goto } from "$app/navigation";
  import Fieldset from "$lib/components/forms/fieldset.svelte";

  export let structure, parent;

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
        structureSlug: structure.slug,
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
</script>

<svelte:head>
  <title>Invitation | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <AuthLayout>
    <Fieldset title="Invitation">
      <p>
        Vous avez reçu une invitation pour rejoindre la structure
        suivante&nbsp;:
      </p>
      <div>
        <div class="mb-s0 border border-gray-01 p-s24">
          <h3 class="text-gray-text">{structure.name}</h3>
          {#if structure.siret}
            <div class="legend">{structure.siret}</div>
          {/if}
          <div class="legend">{structure.address1}</div>
          <div class="legend">{structure.address2}</div>
          <div class="legend">
            {structure.postalCode}
            {structure.city}
          </div>
        </div>
        {#if parent}
          <div class="mt-s0 border border-t-0 border-gray-01 bg-gray-bg p-s24">
            <p class="legend mb-s8">
              Cette structure est une antenne de&nbsp;:
            </p>
            <h4 class="mb-s8 text-gray-text">{parent.name}</h4>
            <div class="legend">{parent.siret}</div>
            <div class="legend">
              {#if parent.address1}{parent.address1}{/if}{#if parent.address2}
                {parent.address2}{/if}{#if parent.address1 || parent.address2},{/if}
              {parent.postalCode}
              {parent.city}
            </div>
          </div>
        {/if}
      </div>
      <div class="mt-s24">
        <div class="legend">
          En cliquant sur
          <span class="italic">Adhérer à la structure</span>, je déclare faire
          partie de la structure mentionnée ci-dessus et j’atteste connaître les
          risques encourus en cas de faux et d’usage de faux.
        </div>

        <div class="mt-s24 flex justify-end">
          <Button
            label="Adhérer à la structure"
            on:click={handleJoin}
            preventDefaultOnMouseDown
          />
        </div>
      </div>
    </Fieldset>
  </AuthLayout>
</EnsureLoggedIn>
