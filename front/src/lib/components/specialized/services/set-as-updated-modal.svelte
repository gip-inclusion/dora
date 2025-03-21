<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import { checkboxCircleFillIcon, editIcon } from "$lib/icons";
  import { markServiceAsSynced } from "$lib/requests/services";
  import type { Service, ServicesOptions, ShortService } from "$lib/types";
  import ServiceContact from "./display/service-contact.svelte";
  import ExtendedServiceKeyInformations from "./display/extended-service-key-informations.svelte";

  export let isOpen = false;
  export let service: Service | ShortService;
  export let servicesOptions: ServicesOptions;
  export let onRefresh: () => Promise<void>;

  async function setAsUpdated() {
    await markServiceAsSynced(service);
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
  width="small"
>
  <div class="pt-s16 text-f18 text-france-blue">
    Périmètre : <strong>{service.diffusionZoneDetailsDisplay}</strong>
  </div>

  <hr class="my-s24" />
  <ServiceContact {service} useWhiteText={false} />
  <hr class="my-s24" />
  <ExtendedServiceKeyInformations {service} {servicesOptions} />

  <div slot="footer">
    <div class="mt-s24 gap-s24 flex flex-col-reverse justify-end md:flex-row">
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
  </div>
</Modal>
