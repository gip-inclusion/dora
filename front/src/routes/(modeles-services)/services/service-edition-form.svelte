<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import FormErrors from "$lib/components/forms/form-errors.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import StickyFormSubmissionRow from "$lib/components/forms/sticky-form-submission-row.svelte";
  import Form, { type FormControls } from "$lib/components/forms/form.svelte";
  import FieldsContact from "$lib/components/specialized/services/fields-contact.svelte";
  import FieldsDuration from "$lib/components/specialized/services/fields-duration.svelte";
  import FieldsPresentation from "$lib/components/specialized/services/fields-presentation.svelte";
  import FieldsDocuments from "../_common/fields-documents.svelte";
  import FieldsModalities from "../_common/fields-modalities.svelte";
  import FieldsPerimeter from "../_common/fields-perimeter.svelte";
  import FieldsPeriodicity from "../_common/fields-periodicity.svelte";
  import FieldsPlace from "$lib/components/specialized/services/fields-place.svelte";
  import FieldsPublics from "$lib/components/specialized/services/fields-publics.svelte";
  import FieldsStructure from "../_common/fields-structure.svelte";
  import FieldsTypology from "$lib/components/specialized/services/fields-typology.svelte";
  import { createOrModifyService } from "$lib/requests/services";
  import type {
    Model,
    Service,
    ServicesOptions,
    ShortStructure,
  } from "$lib/types";
  import { log } from "$lib/utils/logger";
  import { draftSchema, serviceSchema } from "$lib/validation/schemas/service";
  import { validate } from "$lib/validation/validation";
  import DocumentUploadNoticeModal from "./document-upload-notice-modal.svelte";
  import { goto } from "$app/navigation";

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
  let isModalOpen = $state(false);
  let formControls = $state<FormControls>({
    submit: undefined,
    validateForm: undefined,
  });
  const shouldShowModal = $derived(
    (service.credentials?.length ?? 0) > 0 ||
      (service.forms?.length ?? 0) > 0 ||
      !!service.onlineForm
  );

  function handleChange(validatedData) {
    service = { ...service, ...validatedData };
  }

  function handleSubmit(validatedData, kind: RequestKind) {
    requestKind = kind;
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
    event.preventDefault();
    if (shouldShowModal) {
      const { valid } = formControls.validateForm?.(kind) ?? { valid: false };
      if (valid) {
        requestKind = kind;
        isModalOpen = true;
      }
    } else {
      formControls.submit?.(kind);
    }
  }

  function handleModalConfirm() {
    isModalOpen = false;
    formControls.submit?.(requestKind);
  }

  function handleSuccess(result: Service) {
    if (result.status === "PUBLISHED") {
      return goto(`/structures/${result.structure}/services/publication`);
    } else {
      return goto(`/services/${result.slug}`);
    }
  }

  function handleValidate(data, kind?: string) {
    const schema = kind === "draft" ? draftSchema : serviceSchema;
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
</script>

<FormErrors />

<Form
  bind:data={service}
  bind:formControls
  schema={serviceSchema}
  {servicesOptions}
  onChange={handleChange}
  onSubmit={handleSubmit}
  onSuccess={handleSuccess}
  onValidate={handleValidate}
  bind:requesting
>
  <hr />

  <CenteredGrid>
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
    bind:isOpen={isModalOpen}
    onConfirm={handleModalConfirm}
  />
</Form>
