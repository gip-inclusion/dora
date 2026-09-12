<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";

  import Button from "$lib/components/display/button.svelte";
  import SyncIcon from "$lib/assets/icons/ico-sync.svelte";

  import RadioButtonsField from "$lib/components/forms/fields/radio-buttons-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import { currentSchema } from "$lib/validation/validation";
  import OpeningHoursField from "$lib/components/forms/fields/opening-hours-field.svelte";

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

  let showOpeningHoursField = $state(false);
</script>

<FieldSet title="Périodicité" {showModel}>
  {#snippet help()}
    <div>
      <p class="text-f14">
        La durée limitée permet de supendre automatiquement la visibilité du
        service dans les résultat de recherche.
      </p>
    </div>
  {/snippet}
  <FieldModel
    {...fieldModelProps.updateFrequency ?? {}}
    serviceValue={service.updateFrequency}
    type="text"
  >
    <RadioButtonsField
      id="updateFrequency"
      bind:value={service.updateFrequency}
      choices={servicesOptions.updateFrequencies}
      description="À quelle fréquence les informations de votre service changent-elles (description, critères, public, contact) ? Choisissez la période pour être alerté."
    />
  </FieldModel>
  <FieldModel {...fieldModelProps.openingHours ?? {}}>
    {#if showOpeningHoursField}
      <OpeningHoursField
        id="openingHours"
        bind:value={
          () => service.horairesAccueil ?? "",
          (v) => (service.horairesAccueil = v)
        }
      />
    {:else}
      <FieldWrapper vertical id="openingHours" label="Horaires d'accueil">
        <div class="flex-start gap-y-s16 flex w-1/2 flex-col">
          <Button
            small
            noBackground
            noPadding
            icon={SyncIcon}
            label="Utiliser les horaires de la structure"
            onclick={() => {
              showOpeningHoursField = true;
              service.horairesAccueil = service.structureInfo.openingHours;
            }}
            extraClass="mt-s8"
          />
          <span class="text-f14 font-bold">ou</span>
          <Button
            small
            noBackground
            noPadding
            label="Renseigner des horaires pour le service"
            onclick={() => {
              showOpeningHoursField = true;
            }}
            extraClass="flex align-start p-0"
          />
        </div>
      </FieldWrapper>
    {/if}
  </FieldModel>
</FieldSet>
