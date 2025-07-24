<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import SetAsUpdatedModal from "$lib/components/specialized/services/set-as-updated-modal.svelte";
  import { checkboxCircleFillIcon, copyIcon2, editIcon } from "$lib/icons";
  import type { Service, ServicesOptions, ShortService } from "$lib/types";

  interface Props {
    service: Service | ShortService;
    servicesOptions: ServicesOptions;
    onRefresh: () => void | undefined;
  }

  let { service, servicesOptions, onRefresh }: Props = $props();

  let setAsUpdatedModalOpen = $state(false);

  const extraClass = "hover:bg-magenta-cta hover:text-white! justify-start!";
</script>

<div class="flex flex-col items-end">
  {#if service.status === "PUBLISHED" && service.updateNeeded}
    <Button
      label="Marquer comme à jour"
      icon={checkboxCircleFillIcon}
      iconOnRight
      small
      noBackground
      {extraClass}
      onclick={() => (setAsUpdatedModalOpen = true)}
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
      iconOnRight
      noBackground
      small
      {extraClass}
    />

    <LinkButton
      label="Voir le modèle"
      to="/modeles/{service.model}"
      icon={copyIcon2}
      iconOnRight
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
      iconOnRight
      {extraClass}
    />
    {#if !service.useInclusionNumeriqueScheme}
      <LinkButton
        label="Créer un modèle"
        to={`/modeles/creer?service=${service.slug}&structure=${service.structure}`}
        small
        icon={copyIcon2}
        iconOnRight
        noBackground
        {extraClass}
      />
    {/if}
  {/if}
</div>
