<script lang="ts">
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";
  import { copyIcon2, historyLineIcon } from "$lib/icons";
  import ModelMenu from "./model-button-menu.svelte";

  export let model;
  export let readOnly = true;
</script>

<div class="flex flex-col justify-between rounded-ml bg-white shadow-md ">
  <div class="p-s24">
    <div class="flex items-center justify-between text-f14">
      <div class="flex items-center text-gray-dark">
        <div
          class="mr-s8 flex h-s28 w-s28 items-center justify-center rounded-full bg-service-blue text-service-blue-dark"
        >
          <span class="inline-block h-s16 w-s16 fill-current">
            {@html copyIcon2}
          </span>
        </div>
        {model.numServices}
        {model.numServices > 1 ? "services associés" : "service associé"}
      </div>

      <ModelMenu {model} {readOnly} />
    </div>

    <h3 class="m-s0 mt-s12 min-h-[100px] text-f19 font-bold text-france-blue">
      <a href="/modeles/{model.slug}">{model.name}</a>
    </h3>
  </div>

  <div class="border-t border-t-gray-03 p-s24">
    <div class="flex items-center text-f14  text-gray-dark">
      <div
        class="mr-s8 flex h-s28 w-s28 items-center justify-center rounded-full bg-service-blue text-service-blue-dark"
      >
        <span class="inline-block h-s16 w-s16 fill-current">
          {@html historyLineIcon}
        </span>
      </div>
      <RelativeDateLabel date={model.modificationDate} prefix="Mis à jour" />
    </div>
  </div>
</div>
