<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import FieldGroupPublics from "./fieldgroup-publics.svelte";
  import FieldGroupAccessConditions from "./fieldgroup-access-conditions.svelte";
  import FieldGroupModalities from "./fieldgroup-modalities.svelte";
  import FieldGroupPerimeter from "./fieldgroup-perimeter.svelte";
  import type { FieldSetProps } from "$lib/components/specialized/services/types";

  let {
    service = $bindable(),
    model,
    servicesOptions,
  }: FieldSetProps = $props();
</script>

<FieldSet title="Éligibilité au service">
  <FieldGroupPublics bind:service {model} {servicesOptions} />
  <FieldGroupAccessConditions bind:service {model} {servicesOptions} />
  <FieldGroupModalities bind:service {model} {servicesOptions} />
  <FieldGroupPerimeter bind:service {servicesOptions} />
</FieldSet>
