<script lang="ts">
  import CheckboxLineSystem from "svelte-remix/CheckboxLineSystem.svelte";
  import Edit2LineDesign from "svelte-remix/Edit2LineDesign.svelte";

  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import SetAsUpdatedModal from "$lib/components/specialized/services/set-as-updated-modal.svelte";
  import type { Service, ServicesOptions } from "$lib/types";

  interface Props {
    service: Service;
    servicesOptions: ServicesOptions;
    onRefresh: () => void;
  }

  let { service, servicesOptions, onRefresh }: Props = $props();

  let setAsUpdatedModalOpen = $state(false);
</script>

<div class="gap-s16 flex flex-col sm:flex-row">
  {#if service.updateNeeded && service.status === "PUBLISHED"}
    <Button
      secondary
      label="Marquer comme à jour"
      icon={CheckboxLineSystem}
      onclick={() => (setAsUpdatedModalOpen = true)}
    />

    <SetAsUpdatedModal
      bind:isOpen={setAsUpdatedModalOpen}
      {service}
      {servicesOptions}
      {onRefresh}
    />
  {/if}

  <LinkButton
    label="Modifier"
    to="/services/{service.slug}/editer"
    icon={Edit2LineDesign}
  />
</div>
