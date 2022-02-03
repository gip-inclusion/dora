<script>
  import Button from "$lib/components/button.svelte";

  import Modal from "$lib/components/modal.svelte";
  import SuggestionLine from "./_suggestion-line.svelte";

  export let suggestion;
  export let isOpen = false;
  export let onAccept, onReject, onRefresh;
</script>

{#if suggestion}
  <Modal bind:isOpen>
    <div class="min-w-[80vw] rounded-md bg-white p-s40 shadow-md">
      <div class="flex flex-col gap-s8">
        <SuggestionLine
          label="Nom de la structure"
          data={suggestion.structureInfo.name}
        >
          {suggestion.structureInfo.name}
          ({suggestion.structureInfo.department})
          {#if suggestion.structureInfo.new}
            <div
              class="ml-s8 inline-block rounded bg-magenta-brand px-s8 py-s2 text-f12 uppercase leading-20 text-white"
            >
              NOUV.
            </div>
          {/if}</SuggestionLine
        >

        <SuggestionLine label="Soumis par" data={suggestion.creator}>
          {suggestion.creator?.getFullName} ({suggestion.creator?.email})
        </SuggestionLine>

        <SuggestionLine
          label="Titre du service"
          data={suggestion.serviceInfo.name}
        />

        <SuggestionLine
          label="Présentation résumée"
          data={suggestion.serviceInfo.shortDesc}
        />

        <SuggestionLine
          label="Descriptif complet du service"
          data={suggestion.serviceInfo.fullDesc}
          verticalLayout
        >
          <div class="m-s16 border-l-8 border-gray-02 pl-s16">
            {@html suggestion.serviceInfo.fullDesc}
          </div>
        </SuggestionLine>

        <SuggestionLine
          label="Thématique"
          data={suggestion.serviceInfo.categoryDisplay}
        />

        <SuggestionLine
          label="Besoin(s) auxquels ce service répond"
          data={suggestion.serviceInfo.subcategoriesDisplay}
          isList
        />

        <SuggestionLine
          label="Type de service"
          data={suggestion.serviceInfo.kindsDisplay}
          isList
        />

        <SuggestionLine
          label="Critères d’accès"
          data={suggestion.serviceInfo.accessConditionsDisplay}
          isList
        />

        <SuggestionLine
          label="Publics concernés"
          data={suggestion.serviceInfo.concernedPublicDisplay}
          isList
        />

        <SuggestionLine
          label="Pré-requis"
          data={suggestion.serviceInfo.requirementsDisplay}
          isList
        />

        <SuggestionLine
          label="Service cumulable"
          data={suggestion.serviceInfo.isCumulative}
          isBool
        />

        <SuggestionLine
          label="Frais à charge du bénéficiaire"
          data={suggestion.serviceInfo.hasFee}
          isBool
        />

        <SuggestionLine
          label="Détail des frais"
          verticalLayout
          data={suggestion.serviceInfo.feeDetails}
        >
          <div class="m-s16 border-l-8 border-gray-02 pl-s16">
            {suggestion.serviceInfo.feeDetails}
          </div>
        </SuggestionLine>

        <SuggestionLine
          label="Nom du contact"
          data={suggestion.serviceInfo.contactName}
        />

        <SuggestionLine
          label="Numéro de téléphone"
          data={suggestion.serviceInfo.contactPhone}
        />

        <SuggestionLine
          label="Courriel"
          data={suggestion.serviceInfo.contactEmail}
        />

        <SuggestionLine
          label="Lieu de déroulement"
          data={suggestion.serviceInfo.locationKindsDisplay}
          isList
        />

        <SuggestionLine
          label="Lien visioconférence"
          data={suggestion.serviceInfo.remoteUrl}
        />

        <SuggestionLine label="Ville" data={suggestion.serviceInfo.city} />

        <SuggestionLine
          label="Adresse"
          data={suggestion.serviceInfo.address1}
        />

        <SuggestionLine
          label="Complément d’adresse"
          data={suggestion.serviceInfo.address2}
        />

        <SuggestionLine
          label="Code postal"
          data={suggestion.serviceInfo.postalCode}
        />
      </div>

      <div class="mt-s32 flex flex-row justify-end gap-s16">
        <Button
          label="Rejeter"
          secondary
          on:click={() => onReject(suggestion)}
        />
        <Button label="Valider" on:click={async () => onAccept(suggestion)} />
      </div>
    </div>
  </Modal>
{/if}

<style lang="postcss">
  .line-wrapper {
    @apply flex flex-row;
  }
  .line-wrapper-hz {
    @apply flex flex-col;
  }
  .label {
    @apply mr-s16 w-1/3 font-bold;
  }
  .empty {
    @apply hidden;
  }
</style>
