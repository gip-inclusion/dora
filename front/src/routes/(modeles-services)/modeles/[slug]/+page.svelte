<script lang="ts">
  import { browser } from "$app/environment";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import type { PageData } from "./$types";
  import ModelHeader from "./model-header.svelte";
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";
  import UpdateNeededIcon from "$lib/components/specialized/services/update-needed-icon.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { userInfo } from "$lib/utils/auth";
  import AddCircleFillSystem from "svelte-remix/AddCircleFillSystem.svelte";
  import Edit2LineDesign from "svelte-remix/Edit2LineDesign.svelte";
  import ServiceBody from "../../components/service-body/service-body.svelte";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
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
            icon={Edit2LineDesign}
          />
        {/if}

        {#if $userInfo}
          <LinkButton
            icon={AddCircleFillSystem}
            label="Créer un service"
            to={`/services/creer?modele=${data.model.slug}`}
          />
        {/if}
      </div>
    </div>
  {/if}
  <hr class="mt-s32" />
</CenteredGrid>

<ServiceBody service={data.model} servicesOptions={data.servicesOptions} />
