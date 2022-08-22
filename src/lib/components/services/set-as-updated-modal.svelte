<script lang="ts">
  import Modal from "$lib/components/modal.svelte";
  import type { Service } from "$lib/types";
  import LinkButton from "$lib/components/link-button.svelte";
  import Button from "$lib/components/button.svelte";

  import { checkboxCircleFillIcon, editIcon } from "$lib/icons";
  import ServiceKeyInformations from "./body/service-key-informations.svelte";
  import ServiceContact from "./body/service-contact.svelte";
  import { createOrModifyService } from "$lib/services";

  export let isOpen = false;
  export let service: Service;
  export let onRefresh: () => void;

  async function setAsUpdated() {
    await createOrModifyService(service);
    isOpen = false;
    await onRefresh();
  }
</script>

<Modal
  bind:isOpen
  title="Actualisation"
  subtitle=" Avant de marquer votre service comme à jour, veuillez vérifier que ces
  informations sur le service sont exactes."
  on:close={() => (isOpen = false)}
>
  <div class="mt-s32 text-f18 text-france-blue">
    Périmètre : <strong>{service.diffusionZoneDetailsDisplay}</strong>
  </div>

  <hr class="my-s24" />
  <ServiceContact {service} />
  <hr class="my-s24" />
  <ServiceKeyInformations {service} />
  <hr class="my-s24" />

  <div class="mt-s24 flex flex-col-reverse justify-end gap-s24 md:flex-row">
    <LinkButton
      id="modal-update"
      label="Modifier"
      secondary
      to="/services/{service.slug}/editer"
      icon={editIcon}
    />

    <Button
      id="confirm-updated"
      extraClass="justify-center"
      label="Confirmer"
      icon={checkboxCircleFillIcon}
      on:click={setAsUpdated}
    />
  </div>
</Modal>
