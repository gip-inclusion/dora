<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import FormErrors from "$lib/components/forms/form-errors.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import StickyFormSubmissionRow from "$lib/components/forms/sticky-form-submission-row.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import FieldsContact from "$lib/components/specialized/services/fields-contact.svelte";
  import FieldCategory from "$lib/components/specialized/services/field-category.svelte";
  import FieldsDuration from "$lib/components/specialized/services/fields-duration.svelte";
  import FieldsPresentation from "$lib/components/specialized/services/fields-presentation.svelte";
  import FieldsDocuments from "../_common/fields-documents.svelte";
  import FieldsInclusionNumerique from "../_common/fields-inclusion-numerique.svelte";
  import FieldsModalities from "../_common/fields-modalities.svelte";
  import FieldsPerimeter from "../_common/fields-perimeter.svelte";
  import FieldsPeriodicity from "../_common/fields-periodicity.svelte";
  import FieldsPlace from "$lib/components/specialized/services/fields-place.svelte";
  import FieldsPublics from "$lib/components/specialized/services/fields-publics.svelte";
  import FieldsStructure from "../_common/fields-structure.svelte";
  import FieldsTypology from "$lib/components/specialized/services/fields-typology.svelte";
  import { DI_DORA_UNIFIED_SEARCH_ENABLED } from "$lib/env";
  import { createOrModifyService } from "$lib/requests/services";
  import type {
    Model,
    Service,
    ServicesOptions,
    ShortStructure,
  } from "$lib/types";
  import { log } from "$lib/utils/logger";
  import {
    draftSchema,
    serviceSchema,
    inclusionNumeriqueSchema,
  } from "$lib/validation/schemas/service";
  import { validate } from "$lib/validation/validation";
  import type { Schema } from "$lib/validation/schema-utils";
  import { shortenString } from "$lib/utils/misc";

  export let service: Service;
  export let servicesOptions: ServicesOptions;
  export let managedStructureSearchMode = false;
  export let structures: ShortStructure[];
  export let structure: ShortStructure | undefined;
  export let model: Model | undefined;

  let requesting = false;
  let currentSchema: Schema;

  // Affichage d'un message aux anciennes structures suite à l'ajout d'une limitation du nombre de typologies
  const showMaxCategoriesNotice = (service.categories.length || 0) > 3;

  function handleChange(validatedData) {
    service = { ...service, ...validatedData };
  }

  function preSaveInclusionNumeriqueService(data) {
    data.coachOrientationModes = ["autre"];
    data.coachOrientationModesOther =
      "Mêmes modalités que pour les bénéficiaires";

    data.locationKinds = ["en-presentiel"];
    data.name = "Médiation numérique";

    const proposedServices = servicesOptions.subcategories
      .filter((subcategory) => data.subcategories.includes(subcategory.value))
      .map((subcategory) => subcategory.label.toLowerCase())
      .join(", ");
    data.shortDesc = shortenString(
      `${structure.name} propose des services : ${proposedServices}`,
      280
    );
  }
  function handleSubmit(validatedData, kind) {
    if (service.useInclusionNumeriqueScheme) {
      preSaveInclusionNumeriqueService(validatedData);
    }
    if (kind === "publish") {
      return createOrModifyService({
        ...validatedData,
        status: "PUBLISHED",
        markSynced: true,
      });
    } else if (kind === "draft") {
      return createOrModifyService({
        ...validatedData,
        status: "DRAFT",
        markSynced: true,
      });
    } else {
      log(`Soumission de type ${kind} invalide`);
      return null;
    }
  }

  function handleSuccess(result: Service) {
    if (DI_DORA_UNIFIED_SEARCH_ENABLED && result.status === "PUBLISHED") {
      goto(`/structures/${result.structure}/services/publication`);
    } else {
      goto(`/services/${result.slug}`);
    }
  }

  function handleValidate(data, kind: "draft" | "publish") {
    const schema = kind === "draft" ? draftSchema : currentSchema;
    return validate(data, schema, {
      servicesOptions,
      checkRequired: kind !== "draft",
    });
  }

  let modelSlugTmp = null;

  function unsync() {
    modelSlugTmp = service.model;
    service.model = null;
  }

  function sync() {
    service.model = modelSlugTmp;
    modelSlugTmp = null;
  }

  $: currentSchema = service.useInclusionNumeriqueScheme
    ? inclusionNumeriqueSchema
    : serviceSchema;

  $: {
    if (structure?.noDoraForm) {
      servicesOptions.coachOrientationModes =
        servicesOptions.coachOrientationModes.filter(
          (mode) => mode.value !== "formulaire-dora"
        );
    }
  }
</script>

<FormErrors />

<Form
  bind:data={service}
  schema={currentSchema}
  {servicesOptions}
  onChange={handleChange}
  onSubmit={handleSubmit}
  onSuccess={handleSuccess}
  onValidate={handleValidate}
  bind:requesting
>
  <hr />

  <CenteredGrid>
    {#if showMaxCategoriesNotice}
      <div class="mb-s40">
        <Notice
          type="warning"
          title="Votre service comporte plus de 3 thématiques"
        >
          <p class="mb-s0 text-f14">
            Les thématiques permettent de qualifier un service sur Dora et ont
            pour objectif d’identifier les freins spécifiques (et principaux)
            que vous aidez à lever dans le cadre de votre accompagnement.
          </p>
          <p class="mb-s0 text-f14">
            Plus vous êtes précis dans le référencement de votre offre, plus
            vous aidez les personnes accompagnant les publics à identifier le
            bon service ciblé sur leur besoin et plus les demandes d’orientation
            que vous recevez seront qualifiées.
          </p>
        </Notice>
      </div>
    {/if}

    {#if managedStructureSearchMode || structures.length}
      <div class="lg:w-2/3">
        <FieldsStructure
          bind:structure
          bind:service
          bind:servicesOptions
          bind:model
          {managedStructureSearchMode}
          {structures}
        />
      </div>
    {/if}
  </CenteredGrid>

  {#if service?.structure}
    <hr />

    <CenteredGrid>
      {#if service.model}
        <div class="lg:flex lg:items-center lg:justify-between">
          <h3>Synchronisé avec un modèle</h3>
          <Button
            label="Détacher du modèle"
            secondary
            small
            on:click={unsync}
          />
        </div>
      {/if}

      {#if modelSlugTmp}
        <div class="mb-s24">
          <Notice title="Le service est détaché du modèle" type="warning">
            <p class="text-f14">
              Après enregistrement, cette action sera définitive.
            </p>
            <div slot="button">
              <Button
                label="Re-synchroniser avec le modèle"
                secondary
                small
                on:click={sync}
              />
            </div>
          </Notice>
        </div>
      {:else if service.modelChanged}
        <div class="my-s24">
          <Notice title="Le modèle a été mis à jour" type="warning">
            <p class="text-f14">
              Vous pouvez voir ici les modifications et les utiliser sur le
              service.
            </p>
          </Notice>
        </div>
      {/if}

      {#if !service.useInclusionNumeriqueScheme}
        <div class={service.model ? "" : "lg:w-2/3"}>
          <FieldsTypology noTopPadding bind:service {servicesOptions} {model} />

          <FieldsPresentation bind:service {servicesOptions} {model} />

          <FieldsDuration bind:service {servicesOptions} {model} />

          <FieldsPublics bind:service {servicesOptions} {model} />

          <FieldsModalities bind:service {servicesOptions} {model} />

          <FieldsDocuments bind:service {servicesOptions} {model} />

          <FieldsPeriodicity bind:service {servicesOptions} {model} />
        </div>
        <div class="lg:w-2/3">
          <FieldsPerimeter bind:service {servicesOptions} />

          <FieldsPlace bind:service {structure} {servicesOptions} />

          <FieldsContact bind:service />
        </div>
      {:else}
        <div class={service.model ? "" : "lg:w-2/3"}>
          <Fieldset noTopPadding>
            <FieldCategory bind:service {servicesOptions} {model} />
          </Fieldset>

          <FieldsInclusionNumerique
            bind:service
            {servicesOptions}
            {structure}
          />
        </div>
      {/if}
    </CenteredGrid>

    <StickyFormSubmissionRow>
      <Button
        id="draft"
        type="submit"
        label="Enregistrer en brouillon"
        secondary
        disabled={requesting}
      />

      <Button
        id="publish"
        type="submit"
        label="Publier"
        disabled={requesting}
      />
    </StickyFormSubmissionRow>
  {/if}
</Form>
