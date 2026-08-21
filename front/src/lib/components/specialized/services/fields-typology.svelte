<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BooleanRadioButtonsField from "$lib/components/forms/fields/boolean-radio-buttons-field.svelte";
  import RadioButtonsField from "$lib/components/forms/fields/radio-buttons-field.svelte";
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

  <!-- `options` est passé explicitement : `servicesOptions` expose les types sous la clé
       `kinds`, que `getModelInputProps` ne sait pas rapprocher du champ `kind` — sans quoi
       l'encart « Modèle » afficherait la valeur brute au lieu du libellé. -->
  <FieldModel
    {...fieldModelProps.kind ?? {}}
    type="text"
    options={servicesOptions.kinds}
  >
    <RadioButtonsField
      id="kind"
      bind:value={service.kind}
      choices={servicesOptions.kinds}
      description="Sélectionnez la typologie qui correspond le mieux au service."
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
