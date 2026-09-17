<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import FieldgroupTypology from "./fieldgroup-typology.svelte";
  import FieldgroupPresentation from "./fieldgroup-presentation.svelte";
  import type { FieldSetProps } from "$lib/components/specialized/services/types.ts";

  let {
    servicesOptions,
    service = $bindable(),
    model,
    noTopPadding = false,
  }: FieldSetProps = $props();

  let showModel = $derived(!!service.model);
</script>

<FieldSet title="Informations principales" {showModel} {noTopPadding}>
  {#snippet help()}
    <div>
      <p class="text-f14">
        Les informations principales permettent d'identifier votre
        service&nbsp;: c'est ce que verront en premier les bénéficiaires et
        prescripteurs sur la page du service.
      </p>
      <p class="text-f14">
        Renseigner un titre clair et une description simple facilitera la
        compréhension par les personnes qui en ont besoin.
      </p>
    </div>
  {/snippet}

  <FieldgroupPresentation bind:service {servicesOptions} {model} />

  <FieldgroupTypology bind:service {servicesOptions} {model} />
</FieldSet>
