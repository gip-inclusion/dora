<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import { shortenString } from "$lib/utils";
  import {
    homeIcon,
    briefcaseIcon,
    addCircleIcon,
    settingsIcon,
  } from "$lib/icons";
  import Label from "./label.svelte";

  export let structures;
</script>

<style lang="postcss">
  .wrapper {
    display: flex;
    flex-direction: column;
    padding-bottom: var(--s40);
    gap: var(--s12);
  }

  .structure {
    padding: var(--s16);
    background-color: var(--col-white);
    border-radius: var(--s8);
  }
</style>

<CenteredGrid --col-bg="var(--col-gray-00)">
  <div class="wrapper col-start-1 col-span-full">
    {#each structures as structure}
      <div class="structure flex flex-row gap-2">
        <div class="flex-grow flex flex-row items-center">
          <a href="/structures/{structure.slug}">
            <h5>
              {shortenString(structure.name)} ({structure.typologyDisplay})
            </h5>
          </a>
        </div>
        {#if structure.department}
          <Label
            label={structure.department || " "}
            smallIcon
            iconOnLeft
            icon={homeIcon} />
        {/if}
        <Label
          label={`${structure.numServices} fiche(s)`}
          smallIcon
          iconOnLeft
          icon={briefcaseIcon} />
        <LinkButton
          label="Ajouter une offre"
          to="/services/creer"
          icon={addCircleIcon}
          iconOnRight
          noBackground />
        <LinkButton
          label="Modifier"
          to="/structures/{structure.slug}/editer"
          iconOnRight
          icon={settingsIcon}
          noBackground />
      </div>
    {/each}
  </div>
</CenteredGrid>
