<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import { currentSchema } from "$lib/validation/validation";

  interface Props {
    model?: Model;
    servicesOptions: ServicesOptions;
    service: Service;
  }

  let { model, servicesOptions, service = $bindable() }: Props = $props();

  function handleUseModelValue(fieldName: string) {
    service[fieldName] = model ? model[fieldName] : undefined;
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

  let totalHours = $derived(
    isNaN(service.durationWeeklyHours) || isNaN(service.durationWeeks)
      ? 0
      : (service.durationWeeklyHours || 0) * (service.durationWeeks || 0)
  );
</script>

<FieldSet title="Durée de la prestation">
  <Notice titleLevel="h3" type="info">
    <div>
      Ceci correspond à la durée pendant laquelle les bénéficiaires vont être
      mobilisés sur le service.
    </div>
    <div>
      <strong>Exemples&nbsp;:</strong> Pour un atelier ponctuel de 3 h : temps hebdomadaire
      = 3 heures, durée = 1 semaine (même si la durée réelle est inférieure, elle
      sera arrondie à une semaine pour le calcul). Pour un accompagnement total de
      30 h réparties sur 3 semaines : temps hebdomadaire moyen = 10 h, durée = 3 semaines.
    </div>
  </Notice>

  <FieldModel {...fieldModelProps.durationWeeklyHours ?? {}}>
    <BasicInputField
      type="number"
      id="durationWeeklyHours"
      descriptionText="Si moins d’une heure, laisser 1."
      bind:value={service.durationWeeklyHours}
    />
  </FieldModel>

  <FieldModel {...fieldModelProps.durationWeeks ?? {}}>
    <BasicInputField
      type="number"
      id="durationWeeks"
      descriptionText="Si moins d’une semaine, laisser 1."
      bind:value={service.durationWeeks}
    />
  </FieldModel>

  <div class="font-bold">
    Ce qui correspond à un volume horaire total de {totalHours} heure(s), répartie(s)
    sur {service.durationWeeks || 0} semaine(s).
  </div>
</FieldSet>
