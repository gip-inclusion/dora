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
    isModel = false,
  }: FieldSetProps = $props();
</script>

<FieldSet title="Éligibilité au service">
  {#snippet help()}
    <div>
      <p class="text-f14">
        L'éligibilité définit qui peut bénéficier de ce service et comment y
        accéder. Ces informations permettent aux prescripteurs d'orienter les
        bonnes personnes vers votre service et d'éviter les orientations non
        pertinentes.
      </p>
    </div>
  {/snippet}
  <FieldGroupPublics bind:service {model} {servicesOptions} />
  <FieldGroupAccessConditions bind:service {model} {servicesOptions} />
  <FieldGroupModalities bind:service {model} {servicesOptions} isModel />
  {#if !isModel}
    <FieldGroupPerimeter bind:service {servicesOptions} />
  {/if}
</FieldSet>
