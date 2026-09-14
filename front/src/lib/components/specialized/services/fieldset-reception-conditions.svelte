<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import FieldGroupDuration from "$lib/components/specialized/services/fieldgroup-duration.svelte";
  import FieldGroupAddress from "$lib/components/specialized/services/fieldgroup-address.svelte";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import { moveToTheEnd } from "$lib/utils/misc";
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import Button from "$lib/components/display/button.svelte";
  import SyncIcon from "$lib/assets/icons/ico-sync.svelte";

  import OpeningHoursField from "$lib/components/forms/fields/opening-hours-field.svelte";

  import type { FieldSetProps } from "$lib/components/specialized/services/types.ts";
  import type { ShortStructure } from "$lib/types";

  interface Props extends FieldSetProps {
    structure?: ShortStructure;
  }

  let {
    servicesOptions,
    service = $bindable(),
    model = $bindable(),
    structure,
  }: Props = $props();

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
    <FieldGroupAddress bind:entity={service} parent={structure} />
  {/if}
  <FieldGroupDuration bind:service {model} {servicesOptions} />
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
