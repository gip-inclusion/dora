<script lang="ts">
  import { createEventDispatcher, onDestroy, onMount } from "svelte";
  import mapStyle from "./map-style.json?raw"; // Basé sur https://openmaptiles.geo.data.gouv.fr/styles/osm-bright/style.json
  import * as mlgl from "maplibre-gl";

  import "maplibre-gl/dist/maplibre-gl.css";

  const METROPOLE_BB: mlgl.LngLatBoundsLike = [-5, 42, 8, 51];

  interface Props {
    map: mlgl.Map;
  }

  let { map = $bindable() }: Props = $props();

  const dispatch = createEventDispatcher();

  let mapDiv: HTMLElement = $state();

  onMount(() => {
    map = new mlgl.Map({
      container: mapDiv,
      style: JSON.parse(mapStyle),
      center: [1.5, 46.5],
      zoom: 4,
      maxZoom: 17,
    });
    map.fitBounds(METROPOLE_BB, {
      padding: 20,
    });

    map.on("load", () => {
      dispatch("load");
    });
  });

  onDestroy(() => {
    map.remove();
  });
</script>

<div class="h-full w-full" bind:this={mapDiv}></div>
