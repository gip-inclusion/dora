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

  <FieldgroupPresentation {service} {servicesOptions} {model} />

  <FieldgroupTypology {service} {servicesOptions} {model} />
</FieldSet>
