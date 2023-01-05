<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { defaultAcceptHeader, getApiURL } from "$lib/utils/api";
  import { token, validateCredsAndFillUserInfo } from "$lib/utils/auth";
  import { trackJoinStructure } from "$lib/utils/plausible";
  import { get } from "svelte/store";
  import AuthLayout from "../auth-layout.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;

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
        structureSlug: data.structure.slug,
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

<EnsureLoggedIn>
  <AuthLayout>
    <Fieldset title="Invitation">
      <p>
        Vous avez reçu une invitation pour rejoindre la structure
        suivante&nbsp;:
      </p>
      <div>
        <div class="mb-s0 border border-gray-01 p-s24">
          <h3 class="text-gray-text">{data.structure.name}</h3>
          {#if data.structure.siret}
            <div class="legend">{data.structure.siret}</div>
          {/if}
          <div class="legend">{data.structure.address1}</div>
          <div class="legend">{data.structure.address2}</div>
          <div class="legend">
            {data.structure.postalCode}
            {data.structure.city}
          </div>
        </div>
        {#if data.parent}
          <div class="mt-s0 border border-t-0 border-gray-01 bg-gray-bg p-s24">
            <p class="legend mb-s8">
              Cette structure est une antenne de&nbsp;:
            </p>
            <h4 class="mb-s8 text-gray-text">{data.parent.name}</h4>
            <div class="legend">{data.parent.siret}</div>
            <div class="legend">
              {#if data.parent.address1}{data.parent
                  .address1}{/if}{#if data.parent.address2}
                {data.parent
                  .address2}{/if}{#if data.parent.address1 || data.parent.address2},{/if}
              {data.parent.postalCode}
              {data.parent.city}
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
