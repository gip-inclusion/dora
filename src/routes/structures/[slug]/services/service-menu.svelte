<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import SetAsUpdatedModal from "$lib/components/specialized/services/set-as-updated-modal.svelte";
  import { checkboxCircleFillIcon, copyIcon2, editIcon } from "$lib/icons";
  import type {
    Service,
    ServicesOptions,
    ServiceUpdateStatus,
    ShortService,
  } from "$lib/types";

  export let service: Service | ShortService;
  export let servicesOptions: ServicesOptions;
  export let updateStatus: ServiceUpdateStatus | undefined;
  export let onRefresh: () => void | undefined;

  let setAsUpdatedModalOpen = false;

  const extraClass = "hover:bg-magenta-cta hover:!text-white !justify-start";
</script>

<div class="flex flex-col">
  {#if updateStatus && service.status === "PUBLISHED" && updateStatus !== "NOT_NEEDED"}
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
      {servicesOptions}
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
      icon={copyIcon2}
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
    {#if !service.useInclusionNumeriqueScheme}
      <LinkButton
        label="Créer un modèle"
        to={`/modeles/creer?service=${service.slug}&structure=${service.structure}`}
        small
        icon={copyIcon2}
        noBackground
        {extraClass}
      />
    {/if}
  {/if}
</div>
