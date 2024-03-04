<script lang="ts">
  import { browser } from "$app/environment";
  import Modal from "$lib/components/hoc/modal.svelte";

  export let isVideoModalOpen = false;
</script>

{#if browser}
  <Modal
    bind:isOpen={isVideoModalOpen}
    title="Le formulaire d’orientation"
    width="medium"
  >
    <div style="position: relative; padding-top: 50%;">
      <iframe
        title="DORA - Orienter un bénéficiaire"
        width="100%"
        height="100%"
        src="https://tube.numerique.gouv.fr/videos/embed/c620b3c6-d9c8-46aa-8ab6-42b14b3f45a0?subtitle=fr&amp;warningTitle=0&amp;peertubeLink=0&amp;p2p=0"
        frameborder="0"
        allowfullscreen
        sandbox="allow-same-origin allow-scripts allow-popups"
        style="position: absolute; inset: 0px;"
      ></iframe>
    </div>
  </Modal>
{/if}
