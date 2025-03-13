<script lang="ts">
  import { browser } from "$app/environment";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import type { PageData } from "./$types";
  import ModelHeader from "./model-header.svelte";
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";
  import UpdateNeededIcon from "$lib/components/specialized/services/update-needed-icon.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { userInfo } from "$lib/utils/auth";
  import { addCircleIcon, editIcon } from "$lib/icons";
  import ServiceBody from "../../_common/display/service-body.svelte";

  export let data: PageData;
</script>

<CenteredGrid bgColor="bg-blue-light">
  <ModelHeader model={data.model} />
</CenteredGrid>

<CenteredGrid roundedColor="bg-blue-light">
  {#if browser}
    <div
      class="text-gray-text gap-s24 flex flex-col items-center justify-between sm:flex-row"
    >
      <div class="flex items-center">
        <span class="mr-s16">
          <UpdateNeededIcon updateNeeded={false} />
        </span>

        <RelativeDateLabel
          date={data.model.modificationDate}
          prefix="Mis à jour"
        />
      </div>

      <div class="gap-s24 flex flex-col sm:flex-row">
        {#if data.model.canWrite}
          <LinkButton
            label="Modifier"
            to="/modeles/{data.model.slug}/editer"
            secondary
            icon={editIcon}
          />
        {/if}

        {#if $userInfo}
          <LinkButton
            icon={addCircleIcon}
            label="Créer un service"
            to={`/services/creer?modele=${data.model.slug}`}
          />
        {/if}
      </div>
    </div>
  {/if}
  <hr class="mt-s32" />
</CenteredGrid>

<ServiceBody
  service={data.model}
  servicesOptions={data.servicesOptions}
  isModel
/>
