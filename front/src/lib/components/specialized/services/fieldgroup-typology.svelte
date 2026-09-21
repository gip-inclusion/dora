<script lang="ts">
  import FieldGroup from "$lib/components/display/field-group.svelte";
  import RadioButtonsField from "$lib/components/forms/fields/radio-buttons-field.svelte";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldCategory from "./field-category.svelte";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import FieldSubcategory from "./field-subcategory.svelte";
  import { currentSchema } from "$lib/validation/validation";
  import { URL_HELP_SITE } from "$lib/consts";
  import type { FieldGroupProps } from "$lib/components/specialized/services/types";

  let {
    servicesOptions,
    service = $bindable(),
    model,
  }: FieldGroupProps = $props();

  let showModel = $derived(!!service.model);

  function handleUseModelValue(fieldName: string) {
    service[fieldName] = model ? model[fieldName] : undefined;
  }

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

<FieldGroup title="Typologie du service">
  <FieldModel {...fieldModelProps.categories ?? {}} type="array">
    <FieldCategory
      bind:service
      {servicesOptions}
      description="Sélectionnez les thématiques auxquelles le service correspond."
    />
  </FieldModel>
  {#snippet help()}
    <div>
      <p class="mb-s10 text-f14">
        Classez le service par thématique et besoin pour faciliter votre
        référencement et la lisibilité de votre offre auprès de vos partenaires.
      </p>
      <ul class="text-f14 font-bold">
        <li class="mb-s10">
          <a
            href={`${URL_HELP_SITE}article/quelle-thematique-choisir-pour-votre-service-cywvsk/`}
            class="text-magenta-cta hover:underline"
            target="_blank"
            title="Ouverture dans une nouvelle fenêtre"
            rel="noopener"
          >
            Quelle thématique choisir pour votre service ?
          </a>
        </li>
        <li class="mb-s10">
          <a
            href={`${URL_HELP_SITE}article/siae-votre-offre-de-service-sur-dora-jb4405/`}
            class="text-magenta-cta hover:underline"
            target="_blank"
            title="Ouverture dans une nouvelle fenêtre"
            rel="noopener"
          >
            <abbr title="Structures d’insertion par l’activité économique">
              SIAE
            </abbr>&nbsp;:&nbsp;votre offre de service sur Dora
          </a>
        </li>
        <li>
          <a
            href={`${URL_HELP_SITE}article/referencer-votre-offre-de-formation-professionnalisante-ou-qualifiante-sur-dora-1bzkn1k/`}
            class="text-magenta-cta hover:underline"
            target="_blank"
            title="Ouverture dans une nouvelle fenêtre"
            rel="noopener"
          >
            Référencer votre offre de formation professionnalisante ou
            qualifiante sur Dora
          </a>
        </li>
      </ul>
    </div>
  {/snippet}

  <FieldModel
    {...fieldModelProps.subcategories ?? {}}
    showUseButton
    type="array"
  >
    <FieldSubcategory
      bind:service
      {servicesOptions}
      description="Sélectionnez au moins un besoin, pour chaque thématique choisie."
    />
  </FieldModel>

  <FieldModel {...fieldModelProps.kind ?? {}} type="text">
    <RadioButtonsField
      id="kind"
      bind:value={service.kind}
      choices={servicesOptions.kinds}
      description="Sélectionnez la typologie qui correspond le mieux au service."
    />
  </FieldModel>
</FieldGroup>
