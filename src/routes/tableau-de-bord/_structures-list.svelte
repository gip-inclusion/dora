<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import Label from "$lib/components/label.svelte";
  import { shortenString } from "$lib/utils";
  import {
    homeIcon,
    // briefcaseIcon,
    addCircleIcon,
    settingsIcon,
  } from "$lib/icons";

  export let structures;
</script>

<CenteredGrid --col-bg="var(--col-gray-00)" topPadded>
  <div class="col-start-1 col-span-full flex flex-col pb-s40 gap-s12">
    {#each structures as structure}
      <div class="flex flex-row gap-s16 p-s16 bg-white rounded-md">
        <div class="grow flex flex-row items-center">
          <a href="/tableau-de-bord/structures/{structure.slug}">
            <h5>
              {shortenString(structure.name)}
              {#if structure.typologyDisplay}({structure.typologyDisplay}){/if}
            </h5>
          </a>
        </div>
        {#if structure.department}
          <Label
            label={structure.department || " "}
            smallIcon
            iconOnLeft
            icon={homeIcon}
          />
        {/if}
        <!-- <Label
          label={`${structure.numServices} fiche(s)`}
          smallIcon
          iconOnLeft
          icon={briefcaseIcon} /> -->
        <LinkButton
          label="Ajouter un service"
          to="/services/creer"
          icon={addCircleIcon}
          iconOnRight
          noBackground
        />
        <LinkButton
          label="Gérer"
          to="/tableau-de-bord/structures/{structure.slug}"
          iconOnRight
          icon={settingsIcon}
          noBackground
        />
      </div>
    {/each}
  </div>
</CenteredGrid>
