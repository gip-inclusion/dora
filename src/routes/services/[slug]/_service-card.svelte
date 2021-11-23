<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import AccessBox from "./_access-box.svelte";
  import ModalitiesBox from "./_modalities-box.svelte";
  import OrientationBox from "./_orientation-box.svelte";
  import ServiceHeader from "./_service-header.svelte";
  import ServicePresentation from "./_service-presentation.svelte";
  import Label from "$lib/components/label.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
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
    <div class="flex flex-col gap-s24 lg:flex-row-reverse">
      <div class="flex-initial orientation">
        <OrientationBox {service} />
        <div class="flex-col hidden max-w-md gap-s16 mb-s16 lg:flex">
          <h4>{service.structureInfo.name}</h4>
          <Label label={service.structureInfo.shortDesc} italic />
          <LinkButton
            label="Voir l’offre de services complète"
            to="/structures/{service.structure}"
            nogrow
          />
        </div>
      </div>
      <div class="flex-1 service-pres">
        <ServicePresentation {service} />
      </div>
    </div>
    <div class="service-info">
      <ModalitiesBox {service} />
      <AccessBox {service} />
    </div>
  </div>
</CenteredGrid>
