<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import FieldGroupDuration from "$lib/components/specialized/services/fieldgroup-duration.svelte";
  import FieldGroupAddress from "$lib/components/specialized/services/fieldgroup-address.svelte";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import { moveToTheEnd } from "$lib/utils/misc";
  import { currentSchema } from "$lib/validation/validation";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import Button from "$lib/components/display/button.svelte";
  import UseStructureInfoButton from "./use-structure-info-button.svelte";

  import OpeningHoursField from "$lib/components/forms/fields/opening-hours-field.svelte";

  import type { FieldSetProps } from "$lib/components/specialized/services/types.ts";
  import { getModelInputProps } from "$lib/utils/forms";

  let {
    servicesOptions,
    service,
    model = $bindable(),
  }: FieldSetProps = $props();

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

<FieldSet title="Conditions d’accueil">
  <CheckboxesField
    id="locationKinds"
    bind:value={service.locationKinds}
    choices={moveToTheEnd(servicesOptions.locationKinds, "value", "a-distance")}
    description="Lieu de déroulement du service."
  />
  <hr />
  {#if service.locationKinds.includes("en-presentiel")}
    <FieldGroupAddress bind:entity={service} parent={service.structure} />
  {/if}
  <FieldGroupDuration {service} {model} {servicesOptions} />
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
          <UseStructureInfoButton
            onclick={() => {
              showOpeningHoursField = true;
              service = {
                ...service,
                horairesAccueil: service.structureInfo.openingHours,
              };
            }}
            label="les horaires"
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
