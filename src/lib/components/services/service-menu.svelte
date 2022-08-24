<script lang="ts">
  import LinkButton from "$lib/components/link-button.svelte";
  import { checkboxCircleFillIcon, copyIcon, editIcon } from "$lib/icons";
  import {
    type Service,
    type DashboardService,
    SERVICE_UPDATE_STATUS,
  } from "$lib/types";
  import Button from "../button.svelte";
  import SetAsUpdatedModal from "./set-as-updated-modal.svelte";

  export let service: Service | DashboardService;
  export let updateStatus: SERVICE_UPDATE_STATUS | undefined;
  export let onRefresh: () => void | undefined;

  let setAsUpdatedModalOpen = false;

  const extraClass = "hover:bg-magenta-cta hover:!text-white !justify-start";
</script>

<div class="flex flex-col">
  {#if updateStatus && updateStatus !== SERVICE_UPDATE_STATUS.NOT_NEEDED}
    <Button
      label="Marquer comme à jour"
      icon={checkboxCircleFillIcon}
      small
      noBackground
      {extraClass}
      on:click={() => (setAsUpdatedModalOpen = true)}
    />

    <SetAsUpdatedModal
      bind:isOpen={setAsUpdatedModalOpen}
      {service}
      {onRefresh}
    />
  {/if}

  {#if service.model}
    <LinkButton
      label="Modifier"
      to="/services/{service.slug}/editer"
      icon={editIcon}
      noBackground
      small
      {extraClass}
    />

    <LinkButton
      label="Voir le modèle"
      to="/modeles/{service.model}"
      icon={copyIcon}
      noBackground
      small
      {extraClass}
    />
  {:else}
    <LinkButton
      label="Modifier"
      to="/services/{service.slug}/editer"
      small
      noBackground
      icon={editIcon}
      {extraClass}
    />
    <LinkButton
      label="Créer un modèle"
      to={`/modeles/creer?service=${service.slug}&structure=${service.structure}`}
      small
      icon={copyIcon}
      noBackground
      {extraClass}
    />
  {/if}
</div>
