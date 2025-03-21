<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import SetAsUpdatedModal from "$lib/components/specialized/services/set-as-updated-modal.svelte";
  import { checkboxLineIcon, editIcon } from "$lib/icons";
  import type { Service, ServicesOptions } from "$lib/types";

  export let service: Service;
  export let servicesOptions: ServicesOptions;

  export let onRefresh: () => void;

  let setAsUpdatedModalOpen = false;
</script>

<div class="gap-s16 flex flex-col sm:flex-row">
  {#if service.updateNeeded && service.status === "PUBLISHED"}
    <Button
      secondary
      label="Marquer comme à jour"
      icon={checkboxLineIcon}
      on:click={() => (setAsUpdatedModalOpen = true)}
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
    icon={editIcon}
  />
</div>
