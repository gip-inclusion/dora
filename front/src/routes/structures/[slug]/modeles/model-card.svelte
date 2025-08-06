<script lang="ts">
  import FileCopy2LineDocument from "svelte-remix/FileCopy2LineDocument.svelte";
  import HistoryLineSystem from "svelte-remix/HistoryLineSystem.svelte";

  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";
  import ModelMenu from "./model-button-menu.svelte";

  interface Props {
    model: any;
    readOnly?: boolean;
  }

  let { model, readOnly = true }: Props = $props();
</script>

<div class="flex flex-col justify-between rounded-2xl bg-white shadow-md">
  <div class="p-s24">
    <div class="text-f14 flex items-center justify-between">
      <div class="text-gray-dark flex items-center">
        <div
          class="mr-s8 h-s28 w-s28 bg-service-blue text-service-blue-dark flex items-center justify-center rounded-full"
        >
          <span class="h-s16 w-s16 inline-block fill-current">
            <FileCopy2LineDocument size="16" />
          </span>
        </div>
        {model.numServices}
        {model.numServices > 1 ? "services associés" : "service associé"}
      </div>

      <ModelMenu {model} {readOnly} />
    </div>

    <h3 class="m-s0 mt-s12 text-f19 text-france-blue min-h-[100px] font-bold">
      <a href="/modeles/{model.slug}">{model.name}</a>
    </h3>
  </div>

  <div class="border-t-gray-03 p-s24 border-t">
    <div class="text-f14 text-gray-dark flex items-center">
      <div
        class="mr-s8 h-s28 w-s28 bg-service-blue text-service-blue-dark flex items-center justify-center rounded-full"
      >
        <span class="h-s16 w-s16 inline-block fill-current">
          <HistoryLineSystem size="16" />
        </span>
      </div>
      <RelativeDateLabel date={model.modificationDate} prefix="Mis à jour" />
    </div>
  </div>
</div>
