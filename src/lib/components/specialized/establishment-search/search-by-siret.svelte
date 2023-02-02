<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import type { Establishment } from "$lib/types";

  import { getApiURL } from "$lib/utils/api";
  import { siretRegexp } from "$lib/validation/schema-utils";

  export let onEstablishmentChange: (
    establishment: Establishment | null
  ) => void;

  export let establishment: Establishment | null;
  let siretInput = establishment?.siret;
  let siretIsValid = false;
  let serverErrorMsg = "";

  $: siretIsValid = !!siretInput?.match(siretRegexp);

  async function handleValidateSiret() {
    const url = `${getApiURL()}/search-siret/?siret=${encodeURIComponent(
      siretInput
    )}`;

    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });

    if (response.ok) {
      establishment = await response.json();
    } else if (response.status === 404) {
      serverErrorMsg = "SIRET inconnu";
      establishment = null;
    }

    onEstablishmentChange(establishment);
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.code === "Enter") {
      event.preventDefault();
      if (siretIsValid) {
        handleValidateSiret();
      }
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
        on:keydown={handleKeydown}
        bind:value={siretInput}
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
      {#if serverErrorMsg || (siretInput && !siretInput.match(siretRegexp))}
        <div class="mt-s4  text-f12 text-error">
          {#if serverErrorMsg}
            {serverErrorMsg}
          {:else}
            Ce champ doit comporter 14 chiffres ({siretInput.length}/14
            caractères)
          {/if}
        </div>
      {/if}
    </div>
  </div>
</FieldWrapper>
