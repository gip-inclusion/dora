<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import CheckboxCircleFillSystem from "svelte-remix/CheckboxCircleFillSystem.svelte";
  import Edit2LineDesign from "svelte-remix/Edit2LineDesign.svelte";
  import { markServiceAsSynced } from "$lib/requests/services";
  import type { Service, ServicesOptions, ShortService } from "$lib/types";
  import ServiceContact from "./display/service-contact.svelte";
  import ExtendedServiceKeyInformations from "./display/extended-service-key-informations.svelte";

  interface Props {
    isOpen?: boolean;
    service: Service | ShortService;
    servicesOptions: ServicesOptions;
    onRefresh: () => Promise<void>;
  }

  let {
    isOpen = $bindable(false),
    service,
    servicesOptions,
    onRefresh,
  }: Props = $props();

  async function setAsUpdated() {
    await markServiceAsSynced(service);
    isOpen = false;
    await onRefresh();
  }
</script>

<Modal
  bind:isOpen
  title="Actualisation"
  subtitleText=" Avant de marquer votre service comme à jour, veuillez vérifier que ces
  informations sur le service sont exactes."
  width="small"
>
  <div class="pt-s16 text-f18 text-france-blue">
    Périmètre : <strong>{service.diffusionZoneDetailsDisplay}</strong>
  </div>

  <hr class="my-s24" />
  <ServiceContact {service} useWhiteText={false} />
  <hr class="my-s24" />
  <ExtendedServiceKeyInformations {service} {servicesOptions} />

  {#snippet footer()}
    <div>
      <div class="mt-s24 gap-s24 flex flex-col-reverse justify-end md:flex-row">
        <LinkButton
          id="modal-update"
          label="Modifier"
          secondary
          to="/services/{service.slug}/editer"
          icon={Edit2LineDesign}
        />

        <Button
          id="confirm-updated"
          extraClass="justify-center"
          label="Confirmer"
          icon={CheckboxCircleFillSystem}
          onclick={setAsUpdated}
        />
      </div>
    </div>
  {/snippet}
</Modal>
