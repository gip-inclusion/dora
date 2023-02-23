<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BooleanRadioButtonsField from "$lib/components/forms/fields/boolean-radio-buttons-field.svelte";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldCategory from "./field-category.svelte";
  import FieldModel from "./field-model.svelte";
  import FieldSubcategory from "./field-subcategory.svelte";

  export let servicesOptions: ServicesOptions, service: Service;
  export let model: Model | undefined = undefined;
  export let noTopPadding = false;

  $: showModel = !!service.model;

  function handleUseModelValue(fieldName: string) {
    service[fieldName] = model ? model[fieldName] : undefined;
  }

  $: fieldModelProps = model
    ? getModelInputProps({
        service,
        servicesOptions,
        showModel,
        onUseModelValue: handleUseModelValue,
        model,
      })
    : {};
</script>

<FieldSet title="Typologie" {showModel} {noTopPadding}>
  <FieldModel {...fieldModelProps.categories ?? {}} type="array">
    <FieldCategory
      bind:service
      {servicesOptions}
      {model}
      description={!service.useInclusionNumeriqueScheme
        ? "Cochez jusqu’à 3 thématiques principales."
        : ""}
    />
  </FieldModel>
  <div slot="help">
    <p class="mb-s10 text-f14">
      Classez le service par thématiques et besoins pour faciliter votre
      référencement et la lisibilité de votre offre auprès de vos partenaires.
    </p>
    <ul class="text-f14 font-bold">
      <li class="mb-s10">
        <a
          href="https://aide.dora.fabrique.social.gouv.fr/fr/article/quelle-thematique-choisir-pour-votre-service-cywvsk/"
          class="text-magenta-cta hover:underline"
          target="_blank"
          title="Ouverture dans une nouvelle fenêtre"
          rel="noreferrer"
        >
          Quelle thématique choisir pour votre service ?
        </a>
      </li>
      <li class="mb-s10">
        <a
          href="https://aide.dora.fabrique.social.gouv.fr/fr/article/siae-votre-offre-de-service-sur-dora-jb4405/"
          class="text-magenta-cta hover:underline"
          target="_blank"
          title="Ouverture dans une nouvelle fenêtre"
          rel="noreferrer"
        >
          <abbr title="Structures d’insertion par l’activité économique">
            SIAE
          </abbr>&nbsp;:&nbsp;votre offre de service sur Dora
        </a>
      </li>
      <li class="mb-s10">
        <a
          href="https://aide.dora.fabrique.social.gouv.fr/fr/article/referencer-un-service-dinclusion-numerique-sur-dora-et62ua/"
          class="text-magenta-cta hover:underline"
          target="_blank"
          title="Ouverture dans une nouvelle fenêtre"
          rel="noreferrer"
        >
          Référencer un service d’inclusion numérique sur Dora
        </a>
      </li>
      <li>
        <a
          href="https://aide.dora.fabrique.social.gouv.fr/fr/article/referencer-votre-offre-de-formation-professionnalisante-ou-qualifiante-sur-dora-1bzkn1k/"
          class="text-magenta-cta hover:underline"
          target="_blank"
          title="Ouverture dans une nouvelle fenêtre"
          rel="noreferrer"
        >
          Référencer votre offre de formation professionnalisante ou qualifiante
          sur Dora
        </a>
      </li>
    </ul>
  </div>

  <FieldModel
    {...fieldModelProps.subcategories ?? {}}
    showUseButton
    type="array"
  >
    <FieldSubcategory bind:service {servicesOptions} />
  </FieldModel>
  <FieldModel {...fieldModelProps.kinds ?? {}} type="array">
    <CheckboxesField
      id="kinds"
      bind:value={service.kinds}
      choices={servicesOptions.kinds}
    />
  </FieldModel>

  <FieldModel {...fieldModelProps.isCumulative ?? {}} type="boolean">
    <BooleanRadioButtonsField
      id="isCumulative"
      bind:value={service.isCumulative}
      description="Avec d’autres services."
    />
  </FieldModel>
</FieldSet>
