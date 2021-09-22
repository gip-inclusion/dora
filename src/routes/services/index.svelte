<script context="module">
  import { getServices, unPublishDraft } from "$lib/services";

  export async function load({ _page, _fetch, _session, _context }) {
    return {
      props: {
        services: await getServices(),
      },
    };
  }
</script>

<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import {
    checkBoxBlankIcon,
    homeIcon,
    eyeIcon,
    fileCloudIcon,
    fileEditIcon,
    moreIcon,
  } from "$lib/icons";
  import Label from "$lib/components/label.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import Button from "$lib/components/button.svelte";
  import ButtonMenu from "$lib/components/button-menu.svelte";
  import { shortenString } from "$lib/utils";

  export let services = [];

  async function handleUnpublish(service) {
    const result = await unPublishDraft(service.slug);
    service.isDraft = result.isDraft;
    // force reactive update
    services = services;
  }
</script>

<style lang="postcss">
  .wrapper {
    display: flex;
    flex-direction: column;
    padding-top: var(--s8);
    padding-bottom: var(--s40);
    gap: var(--s12);
  }

  .service {
    padding: var(--s16);
    background-color: var(--col-white);
    border-radius: var(--s8);
  }
</style>

<CenteredGrid --col-bg="var(--col-gray-00)">
  <div class="col-start-1 col-span-full text-left">
    <div class="mb-4">
      <h2>Services</h2>
    </div>
    <div class="border-t border-gray-03 py-3/2" />
  </div>
</CenteredGrid>

<CenteredGrid --col-bg="var(--col-gray-00)">
  <div class="wrapper col-start-1 col-span-full">
    {#each services as service}
      <div class="service flex flex-row gap-2">
        <div class="flex-grow flex flex-row items-center">
          <a href="/services/{service.slug}">
            <h5>{shortenString(service.name)}</h5>
          </a>
        </div>
        <Label
          label={`${service.structureInfo.name}`}
          smallIcon
          iconOnLeft
          icon={homeIcon} />

        <Label label={service.department} bold />
        {#if service.isDraft}
          <Label
            label="Brouillon"
            iconOnLeft
            icon={checkBoxBlankIcon}
            smallIcon
            wait
            bold />
        {:else}
          <Label
            label="Publié"
            iconOnLeft
            icon={checkBoxBlankIcon}
            smallIcon
            success
            bold />
        {/if}
        <Label
          label={`${new Date(service.modificationDate).toLocaleString()}`} />
        <div>
          <LinkButton
            to="/services/{service.slug}"
            icon={eyeIcon}
            noBackground />
        </div>
        <div>
          <ButtonMenu icon={moreIcon}>
            {#if !service.isDraft}
              <div>
                <Button
                  label="Désactiver"
                  on:click={() => handleUnpublish(service)}
                  icon={fileCloudIcon}
                  iconOnRight
                  small
                  noBackground />
              </div>
            {/if}
            <div>
              <LinkButton
                label="Modifier"
                to="/services/{service.slug}/edit"
                icon={fileEditIcon}
                iconOnRight
                small
                noBackground />
            </div>
          </ButtonMenu>
        </div>
      </div>
    {/each}
  </div>
</CenteredGrid>
