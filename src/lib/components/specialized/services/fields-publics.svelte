<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import AddableMultiSelectField from "$lib/components/inputs/addable-multiselect-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import type {
    contribSchema,
    modelSchema,
    serviceSchema,
  } from "$lib/validation/schemas/service";

  import FieldModel from "./field-model.svelte";

  export let servicesOptions: ServicesOptions;
  export let canAddChoices = true;
  export let schema:
    | typeof serviceSchema
    | typeof modelSchema
    | typeof contribSchema;
  export let service: Service;
  export let model: Model | undefined = undefined;

  $: showModel = !!service.model;

  function handleUseModelValue(fieldName: string) {
    service[fieldName] = model ? model[fieldName] : undefined;
  }

  $: fieldModelProps = model
    ? getModelInputProps({
        schema: schema,
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
      Publics auxquels le service s’adresse. Vous pouvez ajouter vos propres
      valeurs avec le bouton « Ajouter une autre option ». Si votre service est
      ouvert à tous, sans critères ou prérequis, laissez les champs avec les
      options par défaut.
    </p>
  </div>

  {#if servicesOptions.concernedPublic.length}
    <FieldModel {...fieldModelProps["concernedPublic"]} type="array">
      <AddableMultiSelectField
        id="concernedPublic"
        schema={schema.concernedPublic}
        bind:values={service.concernedPublic}
        structureSlug={service.structure}
        choices={servicesOptions.concernedPublic}
        placeholder="Tous publics"
        placeholderMulti="Sélectionner"
        sort
        description="Plusieurs choix possibles"
        canAdd={canAddChoices}
        addButtonLabel="Ajouter un profil personnalisé"
      />
    </FieldModel>
  {/if}

  {#if servicesOptions.accessConditions.length}
    <FieldModel {...fieldModelProps["accessConditions"]} type="array">
      <AddableMultiSelectField
        id="accessConditions"
        schema={schema.accessConditions}
        bind:values={service.accessConditions}
        structureSlug={service.structure}
        choices={servicesOptions.accessConditions}
        placeholder="Aucun"
        placeholderMulti="Choisir un autre critères d’admission"
        sort
        description="Plusieurs choix possibles"
        canAdd={canAddChoices}
        addButtonLabel="Ajouter un critère personnalisé"
      />
    </FieldModel>
  {/if}

  {#if servicesOptions.requirements.length}
    <FieldModel {...fieldModelProps["requirements"]} type="array">
      <AddableMultiSelectField
        id="requirements"
        schema={schema.requirements}
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
