<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import type { Establishment } from "$lib/types";

  import { getApiURL } from "$lib/utils/api";

  const safirRegexp = /^\d{5}$/u;

  export let onEstablishmentChange: (
    establishment: Establishment | null
  ) => void;
  export let proposedSafir;
  export let establishment: Establishment | null;
  let safirInput = proposedSafir;
  let safirIsValid = false;
  let serverErrorMsg = "";

  $: safirIsValid = !!safirInput?.match(safirRegexp);

  async function handleValidateSafir() {
    const url = `${getApiURL()}/search-safir/?safir=${encodeURIComponent(
      safirInput
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
      serverErrorMsg = "Code Safir inconnu";
      establishment = null;
    }

    onEstablishmentChange(establishment);
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.code === "Enter") {
      event.preventDefault();
      if (safirIsValid) {
        handleValidateSafir();
      }
    }
  }
</script>

<FieldWrapper
  id="safir-select"
  label="Code Safir de votre agence"
  required
  description="Sur 5 chiffres"
  vertical
>
  <slot slot="description" name="description" />

  <div class="flex flex-col">
    <div class="flex flex-row gap-s12">
      <input
        class="h-s48 grow rounded border border-gray-03 px-s12 py-s6 text-f14 placeholder-gray-text-alt outline-none focus:shadow-focus"
        id="safir-select"
        type="text"
        on:input={() => (serverErrorMsg = "")}
        on:keydown={handleKeydown}
        bind:value={safirInput}
        placeholder="12345"
        maxlength="5"
      />

      <Button
        label="Rechercher"
        disabled={!safirIsValid}
        on:click={handleValidateSafir}
        small
      />
    </div>
    <div>
      {#if serverErrorMsg || (safirInput && !safirInput.match(safirRegexp))}
        <div class="mt-s4 text-f12 text-error">
          {#if serverErrorMsg}
            {serverErrorMsg}
          {:else}
            Ce champ doit comporter 5 chiffres ({safirInput.length}/5
            caractères)
          {/if}
        </div>
      {/if}
    </div>
  </div>
</FieldWrapper>
