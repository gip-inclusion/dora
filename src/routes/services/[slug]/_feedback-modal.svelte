<script>
  import Modal from "$lib/components/modal.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import { serviceSubmissionTimeMeter } from "$lib/stores/service-submission-time-meter";

  export let service;
  export let isOpen = false;
</script>

<Modal
  title="Donnez votre avis"
  bind:isOpen
  on:close={() => serviceSubmissionTimeMeter.clear()}
>
  <CenteredGrid bgColor="bg-gray-bg">
    <div class="h-s512">
      <iframe
        src={`https://tally.so/embed/mRGdpK?alignLeft=1&hideTitle=1&transparentBackground=1&service=${service.slug}&temps=${service.fillingDuration}`}
        width="100%"
        height="512"
        frameborder="0"
        marginheight="0"
        marginwidth="0"
        title="Formulaire d'évaluation de la saisie d'un service"
      />
    </div>
  </CenteredGrid>
</Modal>
