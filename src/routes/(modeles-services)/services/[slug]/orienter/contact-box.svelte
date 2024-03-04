<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import OrientationVideo from "$lib/components/specialized/orientation-video.svelte";
  import ContactEmail from "$lib/components/specialized/services/contact-email.svelte";
  import ContactPhone from "$lib/components/specialized/services/contact-phone.svelte";

  export let service;
  export let contactBoxOpen = false;

  let isVideoModalOpen = false;

  function handleShowContactClick() {
    contactBoxOpen = true;
  }
</script>

<OrientationVideo bind:isVideoModalOpen></OrientationVideo>

<div class="flex flex-col gap-s24">
  <div class="block rounded-ml border border-gray-02 p-s24 px-s32">
    <h3 class="text-france-blue">Contact</h3>
    <p class="text-f16">
      En cas de doute, vous pouvez contacter la personne responsable du
      service&nbsp;:
    </p>
    {#if contactBoxOpen}
      <div class="flex flex-col gap-s4">
        {#if service.contactName}
          <p class="mb-s6 mr-s24 text-f17 text-gray-dark">
            <strong>{service.contactName}</strong>
          </p>
        {/if}

        {#if service.contactPhone}
          <ContactPhone {service} />
        {/if}
        <ContactEmail {service} />
      </div>
    {:else}
      <Button
        label="Afficher les informations de contact"
        on:click={handleShowContactClick}
      />
    {/if}
  </div>

  <Notice
    title="Vous utilisez le formulaire d’orientation pour la première fois ?"
    showIcon={false}
  >
    <Button
      slot="button"
      on:click={() => (isVideoModalOpen = true)}
      label="Voir la vidéo de démonstration."
      secondary
    />
  </Notice>
</div>
