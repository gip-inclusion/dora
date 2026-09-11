<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import RichTextField from "$lib/components/forms/fields/rich-text-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import { currentSchema } from "$lib/validation/validation";

  interface Props {
    servicesOptions: ServicesOptions;
    service: Service;
    model?: Model;
    noTopPadding?: boolean;
  }

  let {
    servicesOptions,
    service = $bindable(),
    model,
    noTopPadding = false,
  }: Props = $props();

  let description: RichTextField;

  function handleUseModelValue(fieldName: string) {
    service[fieldName] = model ? model[fieldName] : undefined;
    if (fieldName === "description") {
      description.updateValue(service.description);
    }
  }

  let showModel = $derived(!!service.model);
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

<FieldSet title="Présentation" {showModel} {noTopPadding}>
  {#snippet help()}
    <div>
      <p class="text-f14">
        Le <b>Résumé</b> présente le service en une phrase courte. Il apparait dans
        les résultats de recherche.
      </p>
      <p class="text-f14">
        <strong>Exemple</strong> :
        <i>
          Faciliter vos déplacements en cas de reprise d’emploi ou de formation
          (entretien d’embauche, concours public…)
        </i>
      </p>
      <p class="text-f14">
        Si besoin, détaillez dans la partie
        <b>Description</b>.
      </p>
    </div>
  {/snippet}

  <FieldModel {...fieldModelProps.name ?? {}}>
    <BasicInputField
      id="name"
      bind:value={service.name}
      descriptionText="Entre 3 à 150 caractères. Écriture en minuscules recommandée, sauf pour les acronymes."
      placeholder="Titre du service…"
    />
  </FieldModel>

  <FieldModel {...fieldModelProps.description ?? {}} paddingTop type="markdown">
    <RichTextField
      id="description"
      bind:this={description}
      placeholder="Décrivez simplement le service"
      vertical
      bind:value={service.description}
      description="Privilégier des phrases courtes et un langage simple. Idéalement entre 200 et 2000 caractères. Cette description sera affichée sur la fiche du service et permettra aux utilisateurs de mieux comprendre le service proposé."
    />
  </FieldModel>
</FieldSet>
