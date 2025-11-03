<script lang="ts">
  import type { Snippet } from "svelte";

  import Button from "$lib/components/display/button.svelte";
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import type { Establishment } from "$lib/types";

  import { getApiURL } from "$lib/utils/api";

  const safirRegexp = /^\d{5}$/u;

  interface Props {
    onEstablishmentChange: (establishment: Establishment | null) => void;
    proposedSafir: string;
    establishment: Establishment | null;
    description?: Snippet;
  }

  let {
    onEstablishmentChange,
    proposedSafir,
    establishment = $bindable(),
    description,
  }: Props = $props();

  let safirInput = $state(proposedSafir);
  let serverErrorMsg = $state("");

  let safirIsValid = $derived(!!safirInput?.match(safirRegexp));

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
  descriptionText="Sur 5 chiffres"
  vertical
  {description}
>
  <div class="flex flex-col">
    <div class="gap-s12 flex flex-row">
      <input
        class="h-s48 border-gray-03 px-s12 py-s6 text-f14 placeholder-gray-text-alt focus:shadow-focus grow rounded-sm border outline-hidden"
        id="safir-select"
        type="text"
        oninput={() => (serverErrorMsg = "")}
        onkeydown={handleKeydown}
        bind:value={safirInput}
        placeholder="12345"
        maxlength="5"
      />

      <Button
        label="Rechercher"
        disabled={!safirIsValid}
        onclick={handleValidateSafir}
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
