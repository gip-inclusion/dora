<script>
  import {
    fileCloudIcon,
    fileEditIcon,
    moreIcon,
    checkIcon,
    deleteBinIcon,
  } from "$lib/icons";

  import Button from "$lib/components/button.svelte";
  import ButtonMenu from "$lib/components/button-menu.svelte";

  import LinkButton from "$lib/components/link-button.svelte";

  import {
    convertSuggestionToDraft,
    deleteService,
    unPublishService,
  } from "$lib/services";

  export let service;
  export let onRefresh;

  async function handleUnpublish() {
    await unPublishService(service.slug);
    await onRefresh();
  }

  async function handleConvertToDraft() {
    await convertSuggestionToDraft(service.slug);
    await onRefresh();
  }

  async function handleDelete() {
    if (confirm(`Supprimer la suggestion ${service.name} ?`)) {
      await deleteService(service.slug);
      await onRefresh();
    }
  }
</script>

<ButtonMenu icon={moreIcon} let:onClose={onCloseParent}>
  {#if service.isSuggestion}
    <div>
      <Button
        label="Convertir en brouillon"
        on:click={() => {
          handleConvertToDraft(service);
          onCloseParent();
        }}
        icon={checkIcon}
        iconOnRight
        small
        noBackground
      />
    </div>
    <div>
      <Button
        label="Rejeter"
        on:click={() => {
          handleDelete(service);
          onCloseParent();
        }}
        icon={deleteBinIcon}
        iconOnRight
        small
        noBackground
      />
    </div>
  {:else}
    {#if !service.isDraft}
      <div>
        <Button
          label="Désactiver"
          on:click={() => {
            handleUnpublish(service);
            onCloseParent();
          }}
          icon={fileCloudIcon}
          iconOnRight
          small
          noBackground
        />
      </div>
    {/if}
    <div>
      <LinkButton
        label="Modifier"
        to="/services/{service.slug}/editer"
        icon={fileEditIcon}
        iconOnRight
        small
        noBackground
      />
    </div>
  {/if}
</ButtonMenu>
