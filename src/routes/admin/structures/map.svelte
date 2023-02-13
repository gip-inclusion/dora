<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import mapStyle from "./map-style.json?raw"; // Basé sur https://openmaptiles.geo.data.gouv.fr/styles/osm-bright/style.json
  import * as mlgl from "maplibre-gl";

  const METROPOLE_BB: mlgl.LngLatBoundsLike = [-5, 42, 8, 51];

  let mapDiv: HTMLElement;
  export let map: mlgl.Map;

  onMount(() => {
    const currentMap = new mlgl.Map({
      container: mapDiv,
      style: JSON.parse(mapStyle),
      center: [1.5, 46.5],
      zoom: 4,
      maxZoom: 17,
    });
    currentMap.fitBounds(METROPOLE_BB, {
      padding: 20,
    });

    currentMap.on("load", () => {
      map = currentMap;
    });
  });

  onDestroy(() => {
    map.remove();
  });
</script>

<div class="h-full w-full" bind:this={mapDiv} />
