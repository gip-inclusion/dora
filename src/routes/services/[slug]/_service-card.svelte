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

<CenteredGrid --col-bg="var(--col-france-blue)" topPadded>
  <ServiceHeader {service} {isPreview} />
</CenteredGrid>

<CenteredGrid
  roundedTop
  --col-under-bg="var(--col-france-blue)"
  --col-content-bg="var(--col-bg)"
>
  <div class="col-span-full flex flex-col">
    <div class="flex flex-col gap-s24 lg:flex-row-reverse">
      <div class="orientation flex-initial">
        <OrientationBox {service} />
        <div
          class="mb-s16 hidden max-w-md flex-col items-start gap-s16 lg:flex"
        >
          <h4>{service.structureInfo.name}</h4>
          <Label label={service.structureInfo.shortDesc} italic />
          <LinkButton
            label="Voir l’offre de services complète"
            to="/structures/{service.structure}"
          />
        </div>
      </div>
      <div class="service-pres flex-1">
        <ServicePresentation {service} />
      </div>
    </div>
    <div class="service-info">
      <ModalitiesBox {service} />
      <AccessBox {service} />
    </div>
  </div>
</CenteredGrid>

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
