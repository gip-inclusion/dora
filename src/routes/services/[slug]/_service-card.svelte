<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import AccessBox from "./_access-box.svelte";
  import ModalitiesBox from "./_modalities-box.svelte";
  import OrientationBox from "./_orientation-box.svelte";
  import ServiceHeader from "./_service-header.svelte";
  import ServicePresentation from "./_service-presentation.svelte";
  import Label from "$lib/components/label.svelte";
  // import LinkButton from "$lib/components/link-button.svelte";
  export let service;
  export let isPreview = false;
</script>

<style lang="postcss">
  .service-info {
    display: flex;
    flex-direction: column;
    margin-bottom: var(--s40);
    gap: var(--s24);
  }

  @media print {
    .service-info {
      margin-bottom: 0;
    }
  }
</style>

<CenteredGrid --col-bg="var(--col-france-blue)" topPadded>
  <ServiceHeader {service} {isPreview} />
</CenteredGrid>

<CenteredGrid
  roundedbg
  --col-under-bg="var(--col-france-blue)"
  --col-content-bg="var(--col-bg)"
>
  <div class="flex flex-col col-span-full">
    <div class="flex flex-col gap-3 lg:flex-row-reverse">
      <div class=" orientation">
        <OrientationBox {service} />
        <div class="flex-col hidden gap-2 lg:flex">
          <h4>{service.structureInfo.name}</h4>
          <Label label={service.structureInfo.shortDesc} italic />
          <!-- <div class="noprint">
        <LinkButton
          to="/structures/{service.structure}"
          small
          nogrow
          label="Voir l’offre complète de services" />
      </div> -->
        </div>
      </div>
      <div class=" service-pres">
        <ServicePresentation {service} />
      </div>
    </div>
    <div class=" service-info">
      <ModalitiesBox {service} />
      <AccessBox {service} />
    </div>
  </div>
</CenteredGrid>
<!--
    Champs non utilisés:

    <strong>sous-catégories : </strong>{service.subcategoriesDisplay}
    <strong>Droit commun : </strong>{service.isCommonLaw}
    <strong>Limité dans le temps : </strong>{service.isTimeLimited}
    <strong>Date de début : </strong>{service.startDate}
    <strong>Date de fin : </strong>{service.endDate}
    <strong>Récurrence : </strong>{service.recurrence}
    <strong>Details récurrence : </strong>{service.recurrenceOther}
    <strong>Suspendre au bout de : </strong>{service.suspensionCount}
    <strong>Suspendre le : </strong>{service.suspensionDate}
-->
