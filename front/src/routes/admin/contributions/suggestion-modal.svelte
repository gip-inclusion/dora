<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import { markdownToHTML } from "$lib/utils/misc";
  import Line from "./line.svelte";

  export let suggestion;
  export let isOpen = false;
  export let onAccept, onReject;
</script>

{#if suggestion}
  <Modal bind:isOpen title="Suggestion">
    <div class="gap-s8 flex flex-col">
      <Line label="Nom de la structure" data={suggestion.structureInfo.name}>
        {suggestion.structureInfo.name}
        ({suggestion.structureInfo.department})
        {#if suggestion.structureInfo.new}
          <div
            class="ml-s8 bg-info px-s8 py-s2 text-f12 inline-block rounded-sm leading-20 text-white"
          >
            Nouv.
          </div>
        {/if}</Line
      >

      <Line label="Soumis par" data={suggestion.creator}>
        {suggestion.creator?.getFullName} ({suggestion.creator?.email})
      </Line>

      {#if suggestion.serviceInfo.name}
        <Line label="Titre du service" data={suggestion.serviceInfo.name} />

        <Line
          label="Présentation résumée"
          data={suggestion.serviceInfo.shortDesc}
        />

        <Line
          label="Descriptif complet du service"
          data={markdownToHTML(suggestion.serviceInfo.fullDesc, 2)}
          verticalLayout
        >
          <div class="m-s16 border-gray-02 pl-s16 border-l-8">
            {@html markdownToHTML(suggestion.serviceInfo.fullDesc, 2)}
          </div>
        </Line>

        <Line
          label="Thématiques"
          data={suggestion.serviceInfo.categoriesDisplay.join(", ")}
        />

        <Line
          label="Besoin(s) auxquels ce service répond"
          data={suggestion.serviceInfo.subcategoriesDisplay}
          isList
        />

        <Line
          label="Type de service"
          data={suggestion.serviceInfo.kindsDisplay}
          isList
        />

        <Line
          label="Critères d’accès"
          data={suggestion.serviceInfo.accessConditionsDisplay}
          isList
        />

        <Line
          label="Publics concernés"
          data={suggestion.serviceInfo.concernedPublicDisplay}
          isList
        />

        <Line
          label="Prérequis"
          data={suggestion.serviceInfo.requirementsDisplay}
          isList
        />

        <Line
          label="Service cumulable"
          data={suggestion.serviceInfo.isCumulative}
          isBool
        />

        <Line
          label="Frais à charge"
          data={suggestion.serviceInfo.feeCondition}
        />

        <Line
          label="Détail des frais"
          verticalLayout
          data={suggestion.serviceInfo.feeDetails}
        >
          <div class="m-s16 border-gray-02 pl-s16 border-l-8">
            {suggestion.serviceInfo.feeDetails}
          </div>
        </Line>

        <Line
          label="Nom du contact"
          data={suggestion.serviceInfo.contactName}
        />

        <Line
          label="Numéro de téléphone"
          data={suggestion.serviceInfo.contactPhone}
        />

        <Line label="Courriel" data={suggestion.serviceInfo.contactEmail} />

        <Line
          label="Mode d’accueil"
          data={suggestion.serviceInfo.locationKindsDisplay}
          isList
        />

        <Line
          label="Lien visioconférence"
          data={suggestion.serviceInfo.remoteUrl}
        />

        <Line label="Ville" data={suggestion.serviceInfo.city} />

        <Line label="Adresse" data={suggestion.serviceInfo.address1} />

        <Line
          label="Complément d’adresse"
          data={suggestion.serviceInfo.address2}
        />

        <Line label="Code postal" data={suggestion.serviceInfo.postalCode} />
      {:else}
        Contenu invalide
      {/if}
    </div>

    <div class="mt-s32 gap-s16 flex flex-row justify-end">
      <Button label="Rejeter" secondary on:click={() => onReject(suggestion)} />
      <Button label="Valider" on:click={() => onAccept(suggestion)} />
    </div>
  </Modal>
{/if}
