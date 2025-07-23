<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import { markServicesAsUpToDate } from "$lib/requests/services";
  import {
    hideNotice,
    isNoticeHidden,
  } from "$lib/utils/service-update-notices";

  type ServiceToUpdate = { name: string; slug: string };

  interface Props {
    structureSlug: string;
    servicesToUpdate?: ServiceToUpdate[];
    requesting?: boolean;
    onRefresh: () => void;
  }

  let {
    structureSlug,
    servicesToUpdate = [],
    requesting = $bindable(false),
    onRefresh,
  }: Props = $props();

  const LIST_LENGTH = 3;

  let showAll = $state(false);

  let showNotice = $derived(
    servicesToUpdate.length && !isNoticeHidden("update", structureSlug)
  );

  async function handleMarkServicesAsUpToDate(
    selectedServices: ServiceToUpdate[]
  ) {
    requesting = true;
    await markServicesAsUpToDate(selectedServices);
    await onRefresh();
    requesting = false;
  }
</script>

{#if showNotice}
  <Notice
    title="Un ou plusieurs services n’ont pas été mis à jour récemment"
    type="warning"
  >
    <div class="w-full">
      <p class="text-f14 block">
        Actualisez-les pour que vos services restent visibles et accessibles à
        votre réseau.
      </p>
      <ul class="ml-s16 block list-disc">
        {#each servicesToUpdate as service, index}
          {#if index < LIST_LENGTH || showAll}
            <li class="mb-s12 text-f14 font-bold">
              <a
                class="full-result-link hover:underline"
                href="/services/{service.slug}"
              >
                {service.name}
              </a>
              <Button
                extraClass="ml-s16 text-magenta-cta text-f14! p-s0!"
                noBackground
                noPadding
                disabled={requesting}
                label="Marquer comme à jour"
                onclick={() => handleMarkServicesAsUpToDate([service])}
              />
              <a
                href="/services/{service.slug}/editer"
                class="text-france-blue ml-s10">Modifier</a
              >
            </li>
          {/if}
        {/each}
      </ul>
      {#if servicesToUpdate.length > LIST_LENGTH}
        <div>
          <Button
            extraClass="ml-s16 text-magenta-cta text-f14! p-s0!"
            noBackground
            noPadding
            label={showAll ? "Réduire la liste" : "Voir toute la liste"}
            onclick={() => {
              showAll = !showAll;
            }}
          />
        </div>
      {/if}
    </div>

    <div class="mt-s16 w-full">
      <Button
        label="Tout marquer comme à jour"
        extraClass="py-s8 text-f14! px-s12!"
        onclick={() => handleMarkServicesAsUpToDate(servicesToUpdate)}
      />
      <Button
        secondary
        extraClass="py-s8 text-f14! px-s12!"
        label="Cacher cette fenêtre"
        onclick={() => {
          hideNotice("update", structureSlug);
          showNotice = false;
        }}
      />
    </div>
  </Notice>
{/if}
