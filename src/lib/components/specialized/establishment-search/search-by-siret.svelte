<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import FieldWrapper from "$lib/components/inputs/field-wrapper.svelte";

  import { getApiURL } from "$lib/utils/api";
  import { siretRegexp } from "$lib/validation/schemas/utils";

  export let onEstablishmentChange = null;
  export let siret = "";

  let establishment;
  let siretIsValid = false;
  let serverErrorMsg = "";

  $: siretIsValid = !!siret?.match(siretRegexp);

  async function handleValidateSiret() {
    const url = `${getApiURL()}/search-siret/?siret=${encodeURIComponent(
      siret
    )}`;

    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });

    if (response.ok) {
      establishment = await response.json();
      if (onEstablishmentChange) {
        onEstablishmentChange(establishment);
      }
    } else if (response.status === 404) {
      serverErrorMsg = "SIRET inconnu";
    }
  }
</script>

<FieldWrapper
  id="siret-select"
  label="Numéro SIRET"
  required
  description="Sur 14 chiffres"
  vertical
>
  <slot slot="description" name="description" />

  <div class="flex flex-col">
    <div class="flex flex-row gap-s12">
      <input
        class="h-s48  grow rounded border border-gray-03 px-s12 py-s6 text-f14 placeholder-gray-text-alt outline-none focus:shadow-focus"
        id="siret-select"
        type="text"
        on:input={() => (serverErrorMsg = "")}
        bind:value={siret}
        placeholder="1234567891234"
        maxlength="14"
      />

      <Button
        label="Rechercher"
        disabled={!siretIsValid}
        on:click={handleValidateSiret}
        small
      />
    </div>
    <div>
      {#if serverErrorMsg || (siret && !siret.match(siretRegexp))}
        <div class="mt-s4  text-f12 text-error">
          {#if serverErrorMsg}
            {serverErrorMsg}
          {:else}
            Ce champ doit comporter 14 chiffres ({siret.length}/14 caractères)
          {/if}
        </div>
      {/if}
    </div>
  </div>
</FieldWrapper>
