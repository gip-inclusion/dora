<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import AddableMultiSelectField from "$lib/components/forms/fields/addable-multiselect-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import { currentSchema } from "$lib/validation/validation";
  import { URL_HELP_SITE } from "$lib/consts";

  interface Props {
    servicesOptions: ServicesOptions;
    service: Service;
    model?: Model;
  }

  let { servicesOptions, service = $bindable(), model }: Props = $props();

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

<FieldSet title="Publics" {showModel}>
  <Notice type="info">
    <p class="text-f16 leading-s24 text-gray-dark mb-s0">
      Indiquer ici les profils de publics à qui s’adresse votre service. Si
      votre service est ouvert à toutes et tous, il n’est pas nécessaire de
      sélectionner des profils.
    </p>
    <p class="text-f16 leading-s24 text-gray-dark mb-s0">
      <a
        href={`${URL_HELP_SITE}/article/definir-les-publics-et-criteres-dacces-a-votre-service-tos25n/`}
        class="text-magenta-cta font-bold"
        target="_blank"
        title="Ouverture dans une nouvelle fenêtre"
        rel="noopener"
      >
        Définir les publics et critères d’accès à votre service
      </a>
    </p>
  </Notice>

  {#if servicesOptions.publics.length}
    <FieldModel {...fieldModelProps.publics ?? {}} type="array">
      <AddableMultiSelectField
        id="publics"
        bind:values={service.publics}
        structureSlug={service.structure}
        choices={servicesOptions.publics}
        sort
        description="Si le service n’est pas ouvert à tous les publics, sélectionnez le profil concerné. Plusieurs choix possibles."
        placeholder="Tous publics"
        canAdd={false}
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
        sort
        description="Critères auxquels les bénéficiaires potentiels doivent correspondre. Plusieurs choix possibles."
        placeholder="Aucun"
        canAdd={false}
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
        sort
        description="Prérequis ou compétences auxquels les bénéficiaires potentiels doivent correspondre. Plusieurs choix possibles."
        placeholder="Aucun"
        canAdd={false}
      />
    </FieldModel>
  {/if}
</FieldSet>
