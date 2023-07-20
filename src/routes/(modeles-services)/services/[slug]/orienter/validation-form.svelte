<script lang="ts">
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";

  import { formatFilePath } from "$lib/utils/file";
  import { isNotFreeService } from "$lib/utils/service";
  import { orientationStep1Schema } from "./schema";
  import { orientation } from "./store";

  export let service;

  const excludedConcernedPublicLabels = ["Autre", "Tous publics"];
  const excludedRequirementLabels = ["Aucun", "Sans condition"];

  const concernedPublicChoices = [
    ...service.concernedPublicDisplay
      .map((value) => ({ value: value, label: value }))
      .filter((elt) => !excludedConcernedPublicLabels.includes(elt.value)),
    { value: "Autre", label: "Autre (à préciser)" },
  ];

  // Que l'option "Autre"
  const serviceAcceptsAllPublic = concernedPublicChoices.length === 1;

  const credentialsDisplay = service.credentialsDisplay.filter(
    (elt) => !elt.toLowerCase().includes("vitale")
  );

  const requirementChoices = [
    ...service.requirementsDisplay,
    ...service.accessConditionsDisplay,
  ]
    .map((value) => ({ value: value, label: value }))
    .filter((elt) => !excludedRequirementLabels.includes(elt.value));

  if (requirementChoices.length === 0) {
    orientationStep1Schema.requirements.required = false;
  }

  if (
    concernedPublicChoices.filter((elt) => elt.value !== "Autre").length === 0
  ) {
    orientationStep1Schema.situation.required = false;
  }

  $: if (!$orientation.situation?.includes("Autre")) {
    $orientation.situationOther = "";
  }
</script>

<div>
  {#if service.feeCondition && isNotFreeService(service.feeCondition)}
    <div class="mb-s12">
      <Notice type="info" title="Frais à charge du bénéficiaire">
        {service.feeDetails}
      </Notice>
    </div>
  {/if}

  <Fieldset title="Publics concernés par ce service" noTopPadding>
    <div class="flex flex-col lg:gap-s8">
      {#if serviceAcceptsAllPublic}
        <p class="mb-s0 text-f14 italic text-gray-text">
          Ce service concerne tous les publics
        </p>
      {/if}

      <CheckboxesField
        id="situation"
        choices={concernedPublicChoices}
        description={!serviceAcceptsAllPublic
          ? "Merci de cocher au moins un profil ou situation"
          : ""}
        bind:value={$orientation.situation}
        vertical
      />

      {#if $orientation.situation?.includes("Autre")}
        <p class="mb-s0 text-f14 italic text-gray-text">
          Merci de fournir uniquement des informations relatives au profil de la
          personne et d’éviter les données sensibles. Le motif de l’orientation
          sera détaillé lors de la deuxième étape de ce formulaire.
        </p>

        <TextareaField
          id="situationOther"
          placeholder=""
          bind:value={$orientation.situationOther}
          hideLabel
          vertical
        />
      {/if}
    </div>
  </Fieldset>

  <Fieldset title="Critères et conditions d’accès">
    <div class="flex flex-col lg:gap-s8">
      {#if requirementChoices.length !== 0}
        <CheckboxesField
          id="requirements"
          choices={requirementChoices}
          description="Merci de cocher au moins un critère ou une condition"
          bind:value={$orientation.requirements}
          vertical
        />
      {:else}
        <p class="mb-s0 italic">
          Ce service n’a aucun critère ou conditions d’accès
        </p>
      {/if}
    </div>
  </Fieldset>

  {#if service.onlineForm || service.formsInfo.length || credentialsDisplay.length}
    <Fieldset title="Documents et justificatifs requis">
      <Notice
        type="info"
        titleLevel="h3"
        title="Pensez à récupérer et compléter les documents ou justificatifs requis"
      >
        <p class="text-f14 text-gray-text-alt2">
          Une demande incomplète génère en moyenne un retard de traitement de 2
          semaines.
        </p>
      </Notice>

      <div class="flex flex-row gap-s48">
        {#if service.onlineForm || service.formsInfo.length}
          <div>
            {#if service.formsInfo.length}
              <h4 class="mb-s4">Documents à compléter</h4>
              <p class="text-f12 text-gray-text-alt2">
                Téléchargez et complétez les documents requis
              </p>
              <ul class="mb-s16 list-inside list-disc">
                {#each service.formsInfo as form}
                  <li>
                    <span class="break-word">
                      <a
                        href={form.url}
                        class="text-f16 text-gray-text underline"
                        download
                      >
                        {formatFilePath(form.name)}
                      </a>
                    </span>
                  </li>
                {/each}
              </ul>
            {/if}
            {#if service.onlineForm}
              <h4 class="mb-s4">Liens</h4>
              <p class="text-f12 text-gray-text">
                Informations complémentaires ou formulaires à compléter
              </p>

              <ul class="list-disc pl-s20">
                <li>
                  <span class="break-word">
                    <a
                      rel="noopener"
                      target="_blank"
                      href={service.onlineForm}
                      class="text-f16 text-gray-text underline"
                      title="Ouverture dans une nouvelle fenêtre"
                    >
                      {service.onlineForm}
                    </a>
                  </span>
                </li>
              </ul>
            {/if}
          </div>
        {/if}
        <div>
          <h4 class="mb-s4">Justificatifs à fournir</h4>
          <p class="text-f12 text-gray-text-alt2">
            Liste des documents à récupérer auprès du ou de la bénéficiaire
          </p>

          <ul class="list-inside list-disc">
            {#each credentialsDisplay as creds}
              <li class="text-f16 text-gray-text">{creds}</li>
            {:else}
              <li class="text-f16 text-gray-text">
                <span>Aucun</span>
              </li>
            {/each}
          </ul>
        </div>
      </div>
    </Fieldset>
  {/if}
</div>
