<script lang="ts">
  import { onMount } from "svelte";
  import { browser } from "$app/environment";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import type { PageData } from "./$types";
  import ModelHeader from "./model-header.svelte";
  import { trackModel } from "$lib/utils/plausible";
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";
  import UpdateStatusIcon from "$lib/components/specialized/services/update-status-icon.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { userInfo } from "$lib/utils/auth";
  import { addCircleIcon, editIcon } from "$lib/icons";
  import ServiceBody from "../../_common/display/service-body.svelte";

  export let data: PageData;

  onMount(() => {
    trackModel(data.model);
  });
</script>

<CenteredGrid bgColor="bg-blue-information">
  <ModelHeader model={data.model} />
</CenteredGrid>

<CenteredGrid roundedColor="bg-blue-information" extraClass="mb-s14 w-full">
  {#if browser}
    <div class="flex items-center justify-between text-gray-text">
      <div class="flex items-center">
        <span class="mr-s16">
          <UpdateStatusIcon updateStatus="NOT_NEEDED" />
        </span>

        <RelativeDateLabel
          date={data.model.modificationDate}
          prefix="Mis à jour"
        />
      </div>

      <div class="flex gap-s24">
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
