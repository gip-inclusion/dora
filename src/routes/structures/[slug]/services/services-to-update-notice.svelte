<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import {
    addIgnoredServicesToUpdate,
    updateServicesFromModel,
  } from "$lib/requests/services";
  import type { StructureService } from "$lib/types";
  import {
    hideModelNotice,
    isModelNoticeHidden,
  } from "$lib/utils/service-updates-via-model";

  export let structureSlug: string;
  export let services: StructureService[] = [];
  export let requesting = false;
  export let onRefresh: () => void;

  const LIST_LENGTH = 3;
  let showAll = false;
  $: servicesToUpdate = services.filter(({ modelChanged }) => modelChanged);

  $: showNotice =
    servicesToUpdate.length && !isModelNoticeHidden(structureSlug);
  $: updatedModels = new Set(
    servicesToUpdate.map(({ modelName }) => modelName)
  );

  async function doUpdate(selectedServices: StructureService[]) {
    requesting = true;
    await updateServicesFromModel(selectedServices);
    await onRefresh();
    requesting = false;
  }

  async function reject(modelSlug: string, serviceSlug: string) {
    await addIgnoredServicesToUpdate([{ modelSlug, serviceSlug }]);
    await onRefresh();
  }
  async function rejectAll() {
    await addIgnoredServicesToUpdate(
      servicesToUpdate.map((serv) => ({
        modelSlug: serv.model,
        serviceSlug: serv.slug,
      }))
    );
    await onRefresh();
  }
</script>

{#if showNotice}
  <Notice
    title="Il existe des mises à jour pour {servicesToUpdate.length} de vos services"
    type="info"
  >
    <div class="w-full">
      <p class="block text-f14">
        Suite à la mise à jour
        {updatedModels.size > 1 ? " des modèles " : " du modèle "}
        {Array.from(updatedModels)
          .map((name) => `"${name}"`)
          .join(", ")}, une mise à jour peut être réalisée sur
        {servicesToUpdate.length > 1
          ? "les services suivants"
          : "le service suivant"} :
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
                extraClass="ml-s16 text-magenta-cta !text-f14 !p-s0"
                noBackground
                noPadding
                disabled={requesting}
                label="Mettre à jour"
                on:click={() => doUpdate([service])}
              />
              <Button
                extraClass="ml-s10 text-marianne-red !text-f14 !p-s0"
                noBackground
                noPadding
                disabled={requesting}
                label="Refuser"
                on:click={() => reject(service.model, service.slug)}
              />
            </li>
          {/if}
        {/each}
      </ul>
      {#if servicesToUpdate.length > LIST_LENGTH}
        <div>
          <Button
            extraClass="ml-s16 text-magenta-cta !text-f14 !p-s0"
            noBackground
            noPadding
            label={showAll ? "Réduire la liste" : "Voir toute la liste"}
            on:click={() => {
              showAll = !showAll;
            }}
          />
        </div>
      {/if}
    </div>

    <div class="mt-s16 w-full">
      <Button
        label="Tout mettre à jour"
        extraClass="py-s8 !text-f14 !px-s12"
        on:click={() => doUpdate(servicesToUpdate)}
      />
      <Button
        secondary
        extraClass="py-s8 !text-f14 !px-s12"
        label="Tout refuser"
        on:click={rejectAll}
      />
      <Button
        secondary
        extraClass="py-s8 !text-f14 !px-s12"
        label="Cacher cette fenêtre"
        on:click={() => {
          hideModelNotice(structureSlug);
          showNotice = false;
        }}
      />
    </div>
  </Notice>
{/if}
