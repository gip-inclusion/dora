<script lang="ts">
  import { externalLinkIcon } from "$lib/icons";

  export let cityLabel: string | null;

  $: queryString = cityLabel ? `?cl=${encodeURIComponent(cityLabel)}` : "";
  $: url = `/annuaire-collectivite${queryString}`;
</script>

<div
  class="border-gray-02 p-s32 lg:pr-s64 relative rounded-2xl border shadow-sm"
>
  <h3 class="mb-s12 text-france-blue">
    <a class="full-result-link hover:underline" href={url} target="_blank">
      Annuaire des Collectivités<span
        class="h-s28 w-s28 pl-s6 pt-s8 inline-block fill-current"
        >{@html externalLinkIcon}</span
      >
    </a>
  </h3>
  <p class="mt-s16 text-f16 text-gray-text">
    <a href={url} target="_blank"
      >Toutes les informations officielles des mairies de France sont recensées
      dans l'Annuaire des Collectivités.</a
    >
  </p>
</div>
