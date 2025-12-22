<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BooleanRadioButtonsField from "$lib/components/forms/fields/boolean-radio-buttons-field.svelte";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldCategory from "./field-category.svelte";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import FieldSubcategory from "./field-subcategory.svelte";
  import { currentSchema } from "$lib/validation/validation";
  import { URL_HELP_SITE } from "$lib/consts";

  interface Props {
    servicesOptions: ServicesOptions;
    service: Service | Model;
    model?: Model;
    noTopPadding?: boolean;
  }

  let {
    servicesOptions,
    service = $bindable(),
    model,
    noTopPadding = false,
  }: Props = $props();

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

<FieldSet title="Typologie" {showModel} {noTopPadding}>
  <FieldModel {...fieldModelProps.categories ?? {}} type="array">
    <FieldCategory
      bind:service
      {servicesOptions}
      {model}
      description={!service.useInclusionNumeriqueScheme
        ? "Sélectionnez jusqu’à 3 thématiques auxquelles le service correspond."
        : ""}
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
            href={`${URL_HELP_SITE}/article/quelle-thematique-choisir-pour-votre-service-cywvsk/`}
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
            href={`${URL_HELP_SITE}/article/siae-votre-offre-de-service-sur-dora-jb4405/`}
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
        <li class="mb-s10">
          <a
            href={`${URL_HELP_SITE}/article/referencer-un-service-dinclusion-numerique-sur-dora-et62ua/`}
            class="text-magenta-cta hover:underline"
            target="_blank"
            title="Ouverture dans une nouvelle fenêtre"
            rel="noopener"
          >
            Référencer un service d’inclusion numérique sur Dora
          </a>
        </li>
        <li>
          <a
            href={`${URL_HELP_SITE}/article/referencer-votre-offre-de-formation-professionnalisante-ou-qualifiante-sur-dora-1bzkn1k/`}
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
      description={!service.useInclusionNumeriqueScheme
        ? "Sélectionnez au moins un besoin, pour chaque thématique choisie."
        : "Sélectionnez au moins un besoin."}
    />
  </FieldModel>

  <FieldModel {...fieldModelProps.kinds ?? {}} type="array">
    <CheckboxesField
      id="kinds"
      bind:value={service.kinds}
      choices={servicesOptions.kinds}
      description="Sélectionnez au moins une typologie de service. Plusieurs choix possibles."
    />
  </FieldModel>

  <FieldModel {...fieldModelProps.isCumulative ?? {}} type="boolean">
    <BooleanRadioButtonsField
      id="isCumulative"
      bind:value={service.isCumulative}
      description="Cochez « Non » si le service n’est pas cumulable avec d’autres dispositifs."
    />
  </FieldModel>
</FieldSet>
