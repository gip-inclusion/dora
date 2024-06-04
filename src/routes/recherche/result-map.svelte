<script lang="ts">
  import * as mlgl from "maplibre-gl";
  import Spiderfy from "@nazka/map-gl-js-spiderfy";

  import insane from "insane";

  import circleIcon from "$lib/assets/icons/circle.png";
  import type { ServiceSearchResult } from "$lib/types";
  import Map from "$lib/components/display/map.svelte";

  import type { PageData } from "./$types";

  interface ServiceWithCoords extends ServiceSearchResult {
    coordinates: [number, number];
  }

  export let data: PageData;
  export let filteredServices: ServiceSearchResult[];
  export let onServiceClick: ((slug: string) => void) | undefined = undefined;

  let map: mlgl.Map;
  let popup: mlgl.Popup;
  let spiderfy: Spiderfy;

  $: onSiteServicesWithCoords = filteredServices.filter(
    (service) =>
      service.locationKinds.includes("en-presentiel") &&
      service.distance <= 50 &&
      !!service.coordinates
  ) as ServiceWithCoords[];

  $: zoomToAddress = Boolean(data.lat && data.lon);

  function getPopupContent(feature): string {
    return insane(
      `<strong>${feature.properties.name}</strong><br>${feature.properties.shortDesc}`
    );
  }

  function handleLeafEnter(feature: mlgl.MapGeoJSONFeature) {
    if (feature.geometry.type !== "Point") {
      return;
    }
    const coordinates = feature.geometry.coordinates.slice() as [
      number,
      number,
    ];
    popup.setLngLat(coordinates).setHTML(getPopupContent(feature)).addTo(map);
    popup._update();
  }

  function handleLeafExit(_feature: mlgl.MapGeoJSONFeature) {
    popup.remove();
  }

  function zoomToAddressOrCity() {
    if (zoomToAddress) {
      // Déplacement animé vers les coordonnées de l'adresse avec zoom de niveau 15
      map.flyTo({
        center: [parseFloat(data.lon!), parseFloat(data.lat!)],
        zoom: 15,
      });
    } else {
      // Sauvegarde des limites par défaut (métropole)
      const defaultBounds = map.getBounds();
      // Affectation immédiate des limites de la ville
      map.fitBounds(new mlgl.LngLatBounds(data.cityBounds), { animate: false });
      // Sauvegarde des valeurs de centre et de zoom de la ville
      const center = map.getCenter();
      const zoom = map.getZoom();
      // Réduction du zoom de 2 niveaux
      const newZoom = zoom - 2;
      // Affectation immédiate des limites par défaut (métropole)
      map.fitBounds(defaultBounds, { animate: false });
      // Déplacement animé vers le centre de la ville avec zoom réduit
      map.flyTo({ center, zoom: newZoom });
    }
  }

  async function handleMapLoaded() {
    spiderfy = new Spiderfy(map, {
      minZoomLevel: 14,
      zoomIncrement: 2,
      renderMethod: "3d",
      closeOnLeafClick: false,
      onLeafClick: (feature: mlgl.Feature) => {
        if (onServiceClick) {
          onServiceClick(feature.properties.slug);
        }
      },
    });

    const image = await map.loadImage(circleIcon);
    map.addImage("cluster", image.data);

    map.addSource("servicesSource", {
      type: "geojson",
      promoteId: "slug",
      cluster: true,
      clusterMaxZoom: map.getMaxZoom(),
      clusterRadius: 50,
      data: {
        type: "FeatureCollection",
        features: onSiteServicesWithCoords.map((service) => ({
          type: "Feature",
          properties: {
            ...service,
          },
          geometry: {
            type: "Point",
            coordinates: [service.coordinates[0], service.coordinates[1]],
          },
        })),
      },
    });

    map.addLayer({
      id: "clusters",
      type: "symbol",
      source: "servicesSource",
      layout: {
        "icon-image": "cluster",
        "icon-allow-overlap": true,
      },
    });

    map.addLayer({
      id: "cluster-count",
      type: "symbol",
      source: "servicesSource",
      layout: {
        "text-field": ["get", "point_count"],
        "text-size": 12,
        "text-allow-overlap": true,
      },
      paint: {
        "text-color": "#ffffff",
      },
    });

    map.on("click", "clusters", (evt) => {
      const feature = evt.features && evt.features[0];
      const serviceSlug = feature?.properties.slug;
      if (onServiceClick && serviceSlug) {
        onServiceClick(serviceSlug);
      }
    });

    let lastHovered: mlgl.MapGeoJSONFeature | null = null;
    map.on("mousemove", function (evt) {
      const featuresUnderMouse = map
        .queryRenderedFeatures(evt.point)
        .filter(
          (feat) =>
            feat.layer.id === "clusters" ||
            feat.layer.id.startsWith("clusters-spiderfy-leaf")
        );
      map.getCanvas().style.cursor =
        featuresUnderMouse.length > 0 ? "pointer" : "";
      const serviceFeatures = featuresUnderMouse.filter(
        (feat) => !feat.properties.cluster
      );
      if (serviceFeatures.length > 1) {
        return;
      }
      const feature = serviceFeatures[0];
      if (feature) {
        if (
          !lastHovered ||
          feature.source !== lastHovered.source ||
          feature.id !== lastHovered.id
        ) {
          lastHovered = feature;
          handleLeafEnter(feature);
        }
      } else {
        lastHovered = null;
        handleLeafExit(feature);
      }
    });

    popup = new mlgl.Popup({
      closeButton: false,
      closeOnClick: false,
    });

    spiderfy.applyTo("clusters");

    map.addControl(new mlgl.NavigationControl({ showCompass: false }));

    zoomToAddressOrCity();
  }

  function updateMapContent() {
    if (!map) {
      return;
    }

    const servicesSource = map.getSource("servicesSource") as
      | mlgl.GeoJSONSource
      | undefined;

    if (!servicesSource) {
      return;
    }

    servicesSource.setData({
      type: "FeatureCollection",
      features: onSiteServicesWithCoords.map((service) => ({
        type: "Feature",
        properties: {
          ...service,
        },
        geometry: {
          type: "Point",
          coordinates: [service.coordinates[0], service.coordinates[1]],
        },
      })),
    });
  }

  $: onSiteServicesWithCoords, updateMapContent();
</script>

<Map bind:map on:load={handleMapLoaded} />
