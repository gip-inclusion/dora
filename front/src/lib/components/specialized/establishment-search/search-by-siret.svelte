<script lang="ts">
  import type { Snippet } from "svelte";

  import Button from "$lib/components/display/button.svelte";
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import type { Establishment } from "$lib/types";

  import { customFetch, getApiURL } from "$lib/utils/api";
  import { siretRegexp } from "$lib/validation/schema-utils";

  interface Props {
    onEstablishmentChange: (establishment: Establishment | null) => void;
    establishment: Establishment | null;
    proposedSiret: string;
    description?: Snippet;
  }

  let {
    onEstablishmentChange,
    establishment = $bindable(),
    proposedSiret,
    description,
  }: Props = $props();

  let siretInput = $state(proposedSiret);
  let serverErrorMsg = $state("");

  let siretIsValid = $derived(!!siretInput?.match(siretRegexp));

  async function handleValidateSiret() {
    const url = `${getApiURL()}/search-siret/?siret=${encodeURIComponent(
      siretInput
    )}`;

    const response = await customFetch(url, {
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
  descriptionText="Sur 14 chiffres"
  vertical
  {description}
>
  <div class="flex flex-col">
    <div class="gap-s12 flex flex-row">
      <input
        class="h-s48 border-gray-03 px-s12 py-s6 text-f14 placeholder-gray-text-alt focus:shadow-focus grow rounded-sm border outline-hidden"
        id="siret-select"
        type="text"
        oninput={() => (serverErrorMsg = "")}
        onkeydown={handleKeydown}
        bind:value={siretInput}
        placeholder="1234567891234"
        maxlength="14"
      />

      <Button
        label="Rechercher"
        disabled={!siretIsValid}
        onclick={handleValidateSiret}
        small
      />
    </div>
    <div>
      {#if serverErrorMsg || (siretInput && !siretInput.match(siretRegexp))}
        <div class="mt-s4 text-f12 text-error">
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
