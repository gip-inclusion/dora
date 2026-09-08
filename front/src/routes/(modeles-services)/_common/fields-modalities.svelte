<script lang="ts">
  import { untrack } from "svelte";

  import FieldSet from "$lib/components/display/fieldset.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import RadioButtons from "$lib/components/inputs/radio-buttons.svelte";
  import RadioButtonsField from "$lib/components/forms/fields/radio-buttons-field.svelte";
  import { URL_HELP_SITE } from "$lib/consts";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import { isNotFreeService } from "$lib/utils/service";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import { currentSchema } from "$lib/validation/validation";

  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";

  interface Props {
    servicesOptions: ServicesOptions;
    service: Service;
    model?: Model;
  }

  let { servicesOptions, service = $bindable(), model }: Props = $props();

  function handleUseModelValue(fieldName) {
    service[fieldName] = model ? model[fieldName] : undefined;
    service = { ...service }; // Force le re-rendu
  }

  let showModel = $derived(!!service.model);

  let mobilisationLinkSource: "dora" | "custom" = $state(
    service.mobilisationLink ? "custom" : "dora"
  );

  $effect(() => {
    if (mobilisationLinkSource === "dora") {
      untrack(() => (service.mobilisationLink = null));
    }
  });

  $effect(() => {
    if (!service.mobilisationModes?.includes("utiliser-lien-mobilisation")) {
      untrack(() => {
        mobilisationLinkSource = "dora";
        service.mobilisationLink = null;
      });
    }
  });

  let fieldModelProps = $derived(
    model
      ? getModelInputProps({
          service,
          servicesOptions,
          showModel,
          onUseModelValue: handleUseModelValue,
          model,
          schema: $currentSchema,
        })
      : {}
  );
</script>

<FieldSet title="Modalités" {showModel}>
  {#snippet help()}
    <div>
      <p class="text-f14">Modalités pour mobiliser le service.</p>
    </div>
  {/snippet}
  <Notice
    type="warning"
    title="Modalités d’orientation"
    showIcon={false}
    titleLevel="h3"
  >
    Afin que le service puisse être mobilisable, merci de choisir au moins une
    méthode d’orientation – soit pour l’accompagnateur, soit pour le
    bénéficiaire.
  </Notice>

  <div class="gap-s24 flex flex-col">
    <FieldModel {...fieldModelProps.mobilisableBy ?? {}} type="array">
      <CheckboxesField
        id="mobilisableBy"
        bind:value={
          () => service.mobilisableBy ?? [],
          (value) => (service.mobilisableBy = value)
        }
        choices={[
          { label: "Usagers", value: "usagers" },
          { label: "Professionnels", value: "professionnels" },
        ]}
        description="Plusieurs choix possibles."
      />
    </FieldModel>
    <FieldModel {...fieldModelProps.mobilisationModes ?? {}} type="array">
      <CheckboxesField
        id="mobilisationModes"
        bind:value={
          () => service.mobilisationModes ?? [],
          (value) => (service.mobilisationModes = value)
        }
        choices={[
          { label: "Envoyer un courriel", value: "envoyer-un-courriel" },
          { label: "Se présenter", value: "se-presenter" },
          { label: "Téléphoner", value: "telephoner" },
          {
            label: "Utiliser un formulaire en ligne",
            value: "utiliser-lien-mobilisation",
          },
        ]}
        description="Au moins un mode de mobilisation requis. Plusieurs choix possibles."
      />
    </FieldModel>
    {#if service.mobilisationModes?.includes("utiliser-lien-mobilisation")}
      <div
        class="border-magenta-cta bg-magenta-10 p-s24 gap-s16 flex w-full flex-col self-end border-l-4 lg:w-2/3"
      >
        <h3 class="text-f18 text-gray-dark font-bold">
          Configuration du formulaire
        </h3>
        <RadioButtons
          id="mobilisationLinkSource"
          bind:group={mobilisationLinkSource}
          choices={[
            {
              label: "Formulaire Dora (par défaut)",
              value: "dora",
              link: `${URL_HELP_SITE}article/orienter-un-ou-une-beneficiaire-as9agp/`,
              linkLabel: "En savoir plus sur le formulaire Dora",
            },
            { label: "Votre propre formulaire", value: "custom" },
          ]}
        />
        <FieldModel {...fieldModelProps.mobilisationLink ?? {}}>
          <BasicInputField
            extraClass="bg-white"
            id="mobilisationLink"
            type="url"
            disabled={mobilisationLinkSource === "dora"}
            bind:value={
              () => service.mobilisationLink ?? "",
              (value) => (service.mobilisationLink = value)
            }
            placeholder="https://exemple.fr/mon-formulaire"
            hideLabel
            vertical
          />
        </FieldModel>
      </div>
    {/if}
    <FieldModel {...fieldModelProps.mobilisationDetails ?? {}}>
      <BasicInputField
        id="mobilisationDetails"
        bind:value={
          () => service.mobilisationDetails ?? "",
          (value) => (service.mobilisationDetails = value)
        }
        descriptionText="Ajouter des précisions sur les modes de mobilisation"
        placeholder="Apportez des précisions sur les modalités…"
      />
    </FieldModel>
  </div>

  <div class="gap-s24 flex flex-col">
    <FieldModel
      {...fieldModelProps.feeCondition ?? {}}
      serviceValue={service.feeCondition}
      type="text"
    >
      <RadioButtonsField
        id="feeCondition"
        bind:value={service.feeCondition}
        choices={servicesOptions.feeConditions}
        description="Précisez si le service est gratuit ou payant pour les bénéficiaires."
      />
    </FieldModel>

    {#if isNotFreeService(service.feeCondition)}
      <FieldModel {...fieldModelProps.feeDetails ?? {}}>
        <TextareaField
          id="feeDetails"
          description="Détaillez les frais à la charge des bénéficiaires, y compris leurs montants."
          bind:value={service.feeDetails}
        />
      </FieldModel>
    {/if}
  </div>
</FieldSet>
