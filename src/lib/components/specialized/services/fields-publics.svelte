<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import AddableMultiSelectField from "$lib/components/forms/fields/addable-multiselect-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";

  export let servicesOptions: ServicesOptions;
  export let canAddChoices = true;
  export let service: Service;
  export let model: Model | undefined = undefined;

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

<FieldSet title="Publics" {showModel}>
  <div slot="help">
    <p class="text-f14">
      Publics auxquels le service s’adresse. Si votre service est ouvert à tous,
      sans critère ou prérequis, laissez les champs avec les options par défaut.
    </p>
    <ul class="text-f14 font-bold">
      <li>
        <a
          href="https://aide.dora.inclusion.beta.gouv.fr/fr/article/definir-les-publics-et-criteres-dacces-a-votre-service-tos25n/"
          class="text-magenta-cta"
          target="_blank"
          title="Ouverture dans une nouvelle fenêtre"
          rel="noopener"
        >
          Définir les publics et critères d'accès à votre service
        </a>
      </li>
    </ul>
  </div>

  {#if servicesOptions.concernedPublic.length}
    <FieldModel {...fieldModelProps.concernedPublic ?? {}} type="array">
      <AddableMultiSelectField
        id="concernedPublic"
        bind:values={service.concernedPublic}
        structureSlug={service.structure}
        choices={servicesOptions.concernedPublic}
        placeholder="Tous publics"
        placeholderMulti="Sélectionner"
        sort
        description="Plusieurs choix possibles"
        canAdd={false}
        addButtonLabel="Ajouter un profil personnalisé"
      />
    </FieldModel>
  {/if}

  {#if servicesOptions.accessConditions.length}
    <FieldModel {...fieldModelProps.accessConditions ?? {}} type="array">
      <AddableMultiSelectField
        id="accessConditions"
        bind:values={service.accessConditions}
        structureSlug={service.structure}
        choices={servicesOptions.accessConditions}
        placeholder="Aucun"
        placeholderMulti="Choisir un autre critères d’admission"
        sort
        description="Plusieurs choix possibles"
        canAdd={false}
        addButtonLabel="Ajouter un critère personnalisé"
      />
    </FieldModel>
  {/if}

  {#if servicesOptions.requirements.length}
    <FieldModel {...fieldModelProps.requirements ?? {}} type="array">
      <AddableMultiSelectField
        id="requirements"
        bind:values={service.requirements}
        structureSlug={service.structure}
        choices={servicesOptions.requirements}
        placeholder="Aucun"
        placeholderMulti="Choisir un autre pré-requis"
        sort
        description="Plusieurs choix possibles"
        canAdd={canAddChoices}
        addButtonLabel="Ajouter un pré-requis personnalisé"
      />
    </FieldModel>
  {/if}
</FieldSet>
