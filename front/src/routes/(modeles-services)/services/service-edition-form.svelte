<script lang="ts">
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
  import DocumentUploadNoticeModal from "./document-upload-notice-modal.svelte";

  type RequestKind = "draft" | "publish";

  interface Props {
    service: Service;
    servicesOptions: ServicesOptions;
    managedStructureSearchMode?: boolean;
    structures: ShortStructure[];
    structure?: ShortStructure;
    model?: Model;
  }

  let {
    service = $bindable(),
    servicesOptions = $bindable(),
    managedStructureSearchMode = false,
    structures,
    structure = $bindable(),
    model = $bindable(),
  }: Props = $props();

  let requesting = $state(false);
  let requestKind = $state<RequestKind | undefined>(undefined);
  let currentSchema: Schema = $derived(
    service.useInclusionNumeriqueScheme
      ? inclusionNumeriqueSchema
      : serviceSchema
  );
  let isModalOpen = $state(false);
  let submit = $state<(submitterId?: string) => Promise<void>>();
  let validateForm =
    $state<(submitterId?: string) => { valid: boolean; validatedData: any }>();
  const shouldShowModal = $derived(
    (service.credentials?.length ?? 0) > 0 ||
      (service.forms?.length ?? 0) > 0 ||
      !!service.onlineForm
  );

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
  function handleSubmit(validatedData, kind: RequestKind) {
    requestKind = kind;
    if (service.useInclusionNumeriqueScheme) {
      preSaveInclusionNumeriqueService(validatedData);
    }
    if (requestKind === "publish") {
      return createOrModifyService({
        ...validatedData,
        status: "PUBLISHED",
        markSynced: true,
      });
    } else if (requestKind === "draft") {
      return createOrModifyService({
        ...validatedData,
        status: "DRAFT",
        markSynced: true,
      });
    } else {
      log(`Soumission de type ${requestKind} invalide`);
      return null;
    }
  }

  function handleButtonClick(event: Event, kind: RequestKind) {
    if (shouldShowModal) {
      event.preventDefault();
      const { valid } = validateForm?.(kind) ?? { valid: false };
      if (valid) {
        requestKind = kind;
        isModalOpen = true;
      }
    }
  }

  function handleModalConfirm() {
    isModalOpen = false;
    submit?.(requestKind);
  }

  function handleSuccess(result: Service) {
    if (DI_DORA_UNIFIED_SEARCH_ENABLED && result.status === "PUBLISHED") {
      window.location.href = `/structures/${result.structure}/services/publication`;
    } else {
      window.location.href = `/services/${result.slug}`;
    }
  }

  function handleValidate(data, kind?: string) {
    const schema = kind === "draft" ? draftSchema : currentSchema;
    return validate(data, schema, {
      servicesOptions,
      checkRequired: kind !== "draft",
    });
  }

  let modelSlugTmp = $state(null);

  function unsync() {
    modelSlugTmp = service.model;
    service.model = null;
  }

  function sync() {
    service.model = modelSlugTmp;
    modelSlugTmp = null;
  }

  $effect(() => {
    if (structure?.noDoraForm) {
      servicesOptions.coachOrientationModes =
        servicesOptions.coachOrientationModes.filter(
          (mode) => mode.value !== "formulaire-dora"
        );
    }
  });
</script>

<FormErrors />

<Form
  bind:data={service}
  bind:submit
  bind:validateForm
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
          <Button label="Détacher du modèle" secondary small onclick={unsync} />
        </div>
      {/if}

      {#if modelSlugTmp}
        <div class="mb-s24">
          <Notice title="Le service est détaché du modèle" type="warning">
            <p class="text-f14">
              Après enregistrement, cette action sera définitive.
            </p>
            {#snippet button()}
              <div>
                <Button
                  label="Re-synchroniser avec le modèle"
                  secondary
                  small
                  onclick={sync}
                />
              </div>
            {/snippet}
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
        onclick={(event) => handleButtonClick(event, "draft")}
        label="Enregistrer en brouillon"
        secondary
        disabled={requesting}
        loading={requesting && requestKind === "draft"}
      />

      <Button
        id="publish"
        type="submit"
        onclick={(event) => handleButtonClick(event, "publish")}
        label="Publier"
        disabled={requesting}
        loading={requesting && requestKind === "publish"}
      />
    </StickyFormSubmissionRow>
  {/if}
  <DocumentUploadNoticeModal
    isOpen={isModalOpen}
    onClose={() => (isModalOpen = false)}
    onConfirm={handleModalConfirm}
  />
</Form>
