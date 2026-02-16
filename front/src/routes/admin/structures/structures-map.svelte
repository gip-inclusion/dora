<script lang="ts">
  import insane from "insane";

  import * as mlgl from "maplibre-gl";

  import Map from "$lib/components/display/map.svelte";
  import type { AdminShortStructure } from "$lib/types";

  interface Props {
    filteredStructures?: AdminShortStructure[];
    selectedStructureSlug: string | null;
  }

  let { filteredStructures = [], selectedStructureSlug = $bindable() }: Props =
    $props();

  let map: mlgl.Map | undefined = $state();
  let popup: mlgl.Popup;

  function getPopupContent(feature: mlgl.MapGeoJSONFeature): string {
    return insane(
      `<strong>${feature.properties.name}</strong><br>${feature.properties.shortDesc}`
    );
  }

  function zoomToStructures(features: AdminShortStructure[]) {
    if (!map) {
      return;
    }
    if (features.length) {
      const firstCoordinates: mlgl.LngLatLike = [
        features[0].longitude,
        features[0].latitude,
      ];
      const bounds = features.reduce(
        function (acc: mlgl.LngLatBounds, feature: AdminShortStructure) {
          return acc.extend([feature.longitude, feature.latitude]);
        },
        new mlgl.LngLatBounds(firstCoordinates, firstCoordinates)
      );

      if (bounds) {
        map.fitBounds(bounds, {
          padding: 60,
        });
      }
    }
  }

  function handleMapLoaded() {
    if (!map) {
      return;
    }

    map.addSource("structuresSource", {
      type: "geojson",
      promoteId: "slug",
      data: {
        type: "FeatureCollection",
        features: filteredStructures.map((struct) => ({
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

    map.on(
      "mouseenter",
      "structuresLayer",
      function (evt: mlgl.MapLayerMouseEvent) {
        if (!map || !evt.features || evt.features.length === 0) {
          return;
        }
        // Change the cursor style as a UI indicator.
        map.getCanvas().style.cursor = "pointer";
        const feature = evt.features[0];
        const coordinates = (feature.geometry as any).coordinates.slice();
        selectedStructureSlug = feature.properties.slug;

        // Populate the popup and set its coordinates
        // based on the feature found.
        popup
          .setLngLat(coordinates)
          .setHTML(getPopupContent(feature))
          .addTo(map);
        popup._update();
      }
    );

    map.on("mouseleave", "structuresLayer", function () {
      if (!map) {
        return;
      }
      map.getCanvas().style.cursor = "";
      selectedStructureSlug = null;
      popup.remove();
    });

    map.on("click", "structuresLayer", function (evt) {
      if (!evt.features) {
        return;
      }
      const feature = evt.features[0];
      const windowRef = window.open(
        `/structures/${feature.properties.slug}`,
        "_blank"
      );
      if (windowRef) {
        windowRef.focus();
      }
    });

    zoomToStructures(filteredStructures);
  }

  function updateMapContent(structures: AdminShortStructure[]) {
    if (!map) {
      return;
    }

    const structuresSource = map.getSource("structuresSource") as
      | mlgl.GeoJSONSource
      | undefined;

    if (!structuresSource) {
      return;
    }

    structuresSource.setData({
      type: "FeatureCollection",
      features: structures.map((struct) => ({
        type: "Feature",
        properties: {
          ...struct,
        },
        geometry: {
          type: "Point",
          coordinates: [struct.longitude, struct.latitude],
        },
      })),
    });

    zoomToStructures(structures);
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

  $effect(() => {
    updateHoveredFeature(selectedStructureSlug);
  });

  $effect(() => {
    updateMapContent(filteredStructures);
  });
</script>

<Map bind:map onLoad={handleMapLoaded} />
