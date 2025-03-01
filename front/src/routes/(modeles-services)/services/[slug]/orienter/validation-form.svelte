<script lang="ts">
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";

  import { formatFilePath } from "$lib/utils/file";
  import {
    computeConcernedPublicChoices,
    computeRequirementsChoices,
  } from "$lib/utils/orientation";
  import { isNotFreeService } from "$lib/utils/service";
  import { orientationStep1Schema } from "./schema";
  import { orientation } from "./store";

  export let service;

  // Publics concernés par ce service
  const { concernedPublicChoices, concernedPublicRequired } =
    computeConcernedPublicChoices(service);
  orientationStep1Schema.situation.required = concernedPublicRequired;
  const serviceAcceptsAllPublic = concernedPublicChoices.length === 0;

  // Critères et conditions d’accès
  const { requirementChoices, requirementRequired } =
    computeRequirementsChoices(service);
  orientationStep1Schema.requirements.required = requirementRequired;

  // Justificatifs à fournir
  const credentialsDisplay = (service.credentialsDisplay || []).filter(
    (elt) => !elt.toLowerCase().includes("vitale")
  );
</script>

<div>
  {#if service.feeCondition && isNotFreeService(service.feeCondition)}
    <div class="mb-s12">
      <Notice type="info" title="Frais à charge du bénéficiaire">
        {service.feeDetails != null
          ? service.feeDetails
          : "La structure n’a pas précisé le montant des frais"}
      </Notice>
    </div>
  {/if}

  <Fieldset title="Publics concernés par ce service" noTopPadding>
    <div class="lg:gap-s8 flex flex-col">
      {#if serviceAcceptsAllPublic}
        <p class="mb-s0 italic">Ce service concerne tous les publics</p>
      {:else}
        <CheckboxesField
          id="situation"
          choices={concernedPublicChoices}
          description={!serviceAcceptsAllPublic
            ? "Merci de cocher au moins un profil ou situation"
            : ""}
          bind:value={$orientation.situation}
          vertical
        />
      {/if}
    </div>
  </Fieldset>

  <Fieldset title="Critères et conditions d’accès">
    <div class="lg:gap-s8 flex flex-col">
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

  {#if service.onlineForm || service.formsInfo?.length || credentialsDisplay?.length}
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

      <div class="gap-s48 flex flex-row">
        {#if service.onlineForm || service.formsInfo?.length}
          <div>
            {#if service.formsInfo?.length}
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

              <ul class="pl-s20 list-disc">
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
