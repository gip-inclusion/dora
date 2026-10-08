<script lang="ts">
  import { untrack } from "svelte";

  import FieldGroup from "$lib/components/display/field-group.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import RadioButtons from "$lib/components/inputs/radio-buttons.svelte";
  import { URL_HELP_SITE } from "$lib/consts";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import { currentSchema } from "$lib/validation/validation";

  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import type { FieldGroupProps } from "$lib/components/specialized/services/types";

  let {
    servicesOptions,
    service = $bindable(),
    model,
    isModel,
  }: FieldGroupProps = $props();

  function handleUseModelValue(fieldName) {
    service[fieldName] = model ? model[fieldName] : undefined;
    service = { ...service }; // Force le re-rendu
  }

  let showModel = $derived(!!service.model);

  let mobilisationLinkSource: "dora" | "custom" = $state(
    service.mobilisationLink ? "custom" : "dora"
  );

  let noDoraForm = $derived(!!service.structureInfo?.noDoraForm);

  let usesMobilisationLink = $derived(
    !!service.mobilisationModes?.includes("utiliser-lien-mobilisation")
  );

  // Le formulaire Dora n'a pas d'équivalent en v2 : la préférence est enregistrée
  // via `formulaire-dora` (v1). Le back retire `utiliser-lien-mobilisation` de
  // `mobilisationModes` à l'écriture et le réinjecte à la lecture, pour que
  // `mobilisationModes`/`mobilisationLink` restent valides pour data·inclusion
  // (cf. `_validate_dora_form`).
  function setDoraForm(enabled: boolean) {
    const otherModes = (service.coachOrientationModes ?? []).filter(
      (mode) => mode !== "formulaire-dora"
    );
    service.coachOrientationModes = enabled
      ? [...otherModes, "formulaire-dora"]
      : otherModes;
  }

  $effect(() => {
    if (noDoraForm && mobilisationLinkSource === "dora") {
      untrack(() => (mobilisationLinkSource = "custom"));
    }
  });

  $effect(() => {
    if (usesMobilisationLink && mobilisationLinkSource === "dora") {
      untrack(() => {
        service.mobilisationLink = null;
        setDoraForm(true);
      });
    }
  });

  $effect(() => {
    if (usesMobilisationLink && mobilisationLinkSource === "custom") {
      untrack(() => setDoraForm(false));
    }
  });

  $effect(() => {
    if (!usesMobilisationLink) {
      untrack(() => {
        mobilisationLinkSource = noDoraForm ? "custom" : "dora";
        service.mobilisationLink = null;
        setDoraForm(false);
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

  let mobilisationLinkChoices = $derived(
    noDoraForm
      ? [{ label: "Votre propre formulaire", value: "custom" }]
      : [
          {
            label: "Formulaire Dora (par défaut)",
            value: "dora",
            link: `${URL_HELP_SITE}article/orienter-un-ou-une-beneficiaire-as9agp/`,
            linkLabel: "En savoir plus sur le formulaire Dora",
          },
          { label: "Votre propre formulaire", value: "custom" },
        ]
  );
</script>

<FieldGroup title="Modalités d’orientation" showSeparator={!isModel}>
  <div class="gap-s24 flex flex-col">
    <FieldModel
      {...fieldModelProps.mobilisableBy ?? {}}
      options={servicesOptions.mobilisableBy}
      type="array"
    >
      <CheckboxesField
        id="mobilisableBy"
        bind:value={
          () => service.mobilisableBy ?? [],
          (value) => (service.mobilisableBy = value)
        }
        choices={servicesOptions.mobilisableBy}
        description="Plusieurs choix possibles."
      />
    </FieldModel>
    <FieldModel
      {...fieldModelProps.mobilisationModes ?? {}}
      options={servicesOptions.mobilisationModes}
      type="array"
    >
      <CheckboxesField
        id="mobilisationModes"
        bind:value={
          () => service.mobilisationModes ?? [],
          (value) => (service.mobilisationModes = value)
        }
        choices={servicesOptions.mobilisationModes}
        description="Au moins un mode de mobilisation requis. Plusieurs choix possibles."
      />
    </FieldModel>
    {#if service.mobilisationModes?.includes("utiliser-lien-mobilisation")}
      <FieldModel {...fieldModelProps.mobilisationLink ?? {}}>
        <div
          class="border-magenta-cta bg-magenta-10 p-s24 gap-s16 flex w-full flex-col border-l-4 lg:ml-auto lg:w-2/3"
        >
          <h3 class="text-f18 text-gray-dark font-bold">
            Configuration du formulaire
          </h3>
          <RadioButtons
            id="mobilisationLinkSource"
            bind:group={mobilisationLinkSource}
            choices={mobilisationLinkChoices}
          />
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
        </div>
      </FieldModel>
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
</FieldGroup>
