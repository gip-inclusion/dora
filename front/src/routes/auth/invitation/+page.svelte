<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import CheckboxMark from "$lib/components/display/checkbox-mark.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { defaultAcceptHeader, getApiURL } from "$lib/utils/api";
  import { getToken, validateCredsAndFillUserInfo } from "$lib/utils/auth";
  import AuthLayout from "../auth-layout.svelte";
  import type { PageData } from "./$types";
  import { CGU_VERSION } from "../../(static)/cgu/version";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
  let cguAccepted = $state(false);
  let joinError = $state("");
  let loading = $state(false);

  async function handleJoin() {
    loading = true;

    const targetUrl = `${getApiURL()}/auth/join-structure/`;

    const response = await fetch(targetUrl, {
      method: "POST",
      headers: {
        Accept: defaultAcceptHeader,
        "Content-Type": "application/json",
        Authorization: `Token ${getToken()}`,
      },
      body: JSON.stringify({
        structureSlug: data.structure.slug,
        cguVersion: CGU_VERSION,
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
      loading = false;
    } else {
      try {
        joinError = (await response.json()).detail.message;
      } catch (err) {
        console.error(err);
      } finally {
        loading = false;
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
        <div class="mb-s0 border-gray-01 p-s24 border">
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
          <div class="mt-s0 border-gray-01 bg-gray-bg p-s24 border border-t-0">
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
          <label class="flex flex-row items-start">
            <input bind:checked={cguAccepted} type="checkbox" class="hidden" />
            <CheckboxMark />
            <span class="ml-s16 text-f14 text-gray-text inline-block">
              Je déclare avoir lu les
              <a href="/cgu" class="underline" target="_blank" rel="noopener"
                >Conditions générales d’utilisation</a
              > et faire partie de la structure mentionnée ci-dessus.</span
            >
          </label>
        </div>
        <div class="mt-s24">
          {#if joinError}
            <Notice title={joinError} type="error" />
          {/if}
        </div>
        <div class="mt-s24 flex justify-end">
          <Button
            label="Adhérer à la structure"
            onclick={handleJoin}
            preventDefaultOnMouseDown
            disabled={!cguAccepted || loading}
          />
        </div>
      </div>
    </Fieldset>
  </AuthLayout>
</EnsureLoggedIn>
