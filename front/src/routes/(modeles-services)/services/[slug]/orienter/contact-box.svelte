<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import OrientationVideo from "$lib/components/specialized/orientation-video.svelte";
  import ContactInfo from "./contact-info.svelte";
  import type { Service } from "$lib/types";

  interface Props {
    service: Service;
    isDI: boolean;
  }

  let { service, isDI }: Props = $props();

  const displayContact = service.contactPhone || service.contactEmail;
  let isVideoModalOpen = $state(false);
</script>

<OrientationVideo bind:isVideoModalOpen></OrientationVideo>

<div class="gap-s24 flex flex-col">
  {#if displayContact}
    <div class="border-gray-02 p-s24 px-s32 block rounded-2xl border">
      <h3 class="text-france-blue">Contact</h3>
      <p class="text-f16">
        En cas de doute, vous pouvez contacter la personne responsable du
        service&nbsp;:
      </p>
      <ContactInfo {service} {isDI} />
    </div>
  {/if}

  <Notice
    title="Vous utilisez le formulaire d’orientation pour la première fois ?"
    showIcon={false}
  >
    {#snippet button()}
      <Button
        onclick={() => (isVideoModalOpen = true)}
        label="Voir la vidéo de démonstration."
        secondary
      />
    {/snippet}
  </Notice>
</div>
