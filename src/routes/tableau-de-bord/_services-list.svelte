<script>
  import {
    convertSuggestionToDraft,
    deleteService,
    unPublishService,
  } from "$lib/services";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import {
    checkBoxBlankIcon,
    homeIcon,
    eyeIcon,
    fileCloudIcon,
    fileEditIcon,
    moreIcon,
    checkIcon,
    deleteBinIcon,
  } from "$lib/icons";
  import Label from "$lib/components/label.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import Button from "$lib/components/button.svelte";
  import ButtonMenu from "$lib/components/button-menu.svelte";
  import { shortenString } from "$lib/utils";

  export let services = [];
  export let onRefresh;

  async function handleUnpublish(service) {
    await unPublishService(service.slug);
    await onRefresh();
  }

  async function handleConvertToDraft(service) {
    await convertSuggestionToDraft(service.slug);
    await onRefresh();
  }

  async function handleDelete(service) {
    if (confirm(`Supprimer la suggestion ${service.name} ?`)) {
      await deleteService(service.slug);
      await onRefresh();
    }
  }
</script>

<CenteredGrid --col-bg="var(--col-gray-00)" topPadded>
  <div class="wrapper col-span-full col-start-1">
    {#each services as service}
      <div class="service flex flex-row gap-s16">
        <div class="flex grow flex-row items-center">
          <a href="/services/{service.slug}">
            <h5>{shortenString(service.name)}</h5>
          </a>
        </div>
        <Label
          label={`${service.structureInfo.name}`}
          smallIcon
          icon={homeIcon}
        />

        <Label label={service.department} bold />
        {#if service.isSuggestion}
          <Label
            label="Suggestion"
            icon={checkBoxBlankIcon}
            smallIcon
            error
            bold
          />
        {:else if service.isDraft}
          <Label
            label="Brouillon"
            icon={checkBoxBlankIcon}
            smallIcon
            wait
            bold
          />
        {:else}
          <Label
            label="Publié"
            icon={checkBoxBlankIcon}
            smallIcon
            success
            bold
          />
        {/if}
        <Label
          label={`${new Date(service.modificationDate).toLocaleString()}`}
        />
        <div>
          <LinkButton
            to="/services/{service.slug}"
            icon={eyeIcon}
            noBackground
          />
        </div>
        <div>
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
        </div>
      </div>
    {/each}
  </div>
</CenteredGrid>

<style lang="postcss">
  .wrapper {
    display: flex;
    flex-direction: column;
    padding-bottom: var(--s40);
    gap: var(--s12);
  }

  .service {
    padding: var(--s16);
    background-color: var(--col-white);
    border-radius: var(--s8);
  }
</style>
