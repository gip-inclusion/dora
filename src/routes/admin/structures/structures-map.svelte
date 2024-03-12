<script lang="ts">
  import type { AdminShortStructure, GeoApiValue } from "$lib/types";
  import * as mlgl from "maplibre-gl";
  import "maplibre-gl/dist/maplibre-gl.css";
  import Map from "./map.svelte";
  import insane from "insane";

  export let filteredStructures: AdminShortStructure[] = [];
  export let selectedStructureSlug: string | null;
  export let department: GeoApiValue;

  let map: mlgl.Map;
  let popup: mlgl.Popup;

  function getPopupContent(feature): string {
    return insane(
      `<strong>${feature.properties.name}</strong><br>${feature.properties.shortDesc}`
    );
  }
  function updateMapContent(structs: AdminShortStructure[]) {
    if (!map) {
      return;
    }
    if (map.getLayer("structuresLayer")) {
      map.removeLayer("structuresLayer");
    }
    if (map.getSource("structuresSource")) {
      map.removeSource("structuresSource");
    }

    map.addSource("structuresSource", {
      type: "geojson",
      promoteId: "slug",
      data: {
        type: "FeatureCollection",
        features: structs.map((struct) => ({
          type: "Feature",
          properties: {
            ...struct,
          },
          geometry: {
            type: "Point",
            coordinates: [struct.longitude, struct.latitude],
          },
        })),
      },
    });

    map.addLayer({
      id: "structuresLayer",
      type: "circle",
      source: "structuresSource",
      paint: {
        "circle-radius": 7,
        "circle-color": [
          "case",
          ["boolean", ["feature-state", "hover"], false],
          "#6CB6EB",
          "#3887be",
        ],
        "circle-stroke-color": "#efefef",
        "circle-stroke-width": 0.4,
        "circle-stroke-opacity": 0.5,
        "circle-opacity": 0.8,
      },
    });

    popup = new mlgl.Popup({
      closeButton: false,
      closeOnClick: false,
    });

    map.on("mouseenter", "structuresLayer", function (evt) {
      // Change the cursor style as a UI indicator.
      map.getCanvas().style.cursor = "pointer";
      const feature = evt.features[0];
      const coordinates = feature.geometry.coordinates.slice();
      selectedStructureSlug = feature.properties.slug;

      // Populate the popup and set its coordinates
      // based on the feature found.
      popup.setLngLat(coordinates).setHTML(getPopupContent(feature)).addTo(map);
      popup._update();
    });

    map.on("mouseleave", "structuresLayer", function () {
      map.getCanvas().style.cursor = "";
      selectedStructureSlug = null;
      popup.remove();
    });

    map.on("click", "structuresLayer", function (evt) {
      const feature = evt.features[0];
      window.open(`/structures/${feature.properties.slug}`, "_blank").focus();
    });
  }

  function zoomToStructures(features) {
    if (!map) {
      return;
    }
    if (features.length) {
      const firstCoordinates = [features[0].longitude, features[0].latitude];
      const bounds = features.reduce(
        function (acc, feature) {
          return acc.extend([feature.longitude, feature.latitude]);
        },
        new mlgl.LngLatBounds(firstCoordinates, firstCoordinates)
      );

      if (bounds) {
        map.fitBounds(bounds, {
          padding: 60,
        });
      }
    } else if (department) {
      const coordinates = department.geom.coordinates[0];
      const bounds = coordinates.reduce(
        function (acc, coord) {
          return acc.extend(coord);
        },
        new mlgl.LngLatBounds(coordinates[0], coordinates[0])
      );

      map.fitBounds(bounds, {
        padding: 20,
      });
    }
  }

  function updateHoveredFeature(structureSlug: string | null) {
    if (map) {
      if (map.getSource("structuresSource")) {
        map.removeFeatureState({
          source: "structuresSource",
        });
      }
      if (structureSlug) {
        map.setFeatureState(
          {
            source: "structuresSource",
            id: structureSlug,
          },
          { hover: true }
        );
      }
    }
  }

  $: updateHoveredFeature(selectedStructureSlug);
  $: updateMapContent(filteredStructures);
  $: zoomToStructures(filteredStructures);
</script>

<Map bind:map />
