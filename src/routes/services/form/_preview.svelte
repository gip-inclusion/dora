<script>
  import ServiceCard from "../[slug]/_service-card.svelte";

  export let service;
</script>

<svelte:head>
  <title>Dora: {service.name} par {service?.structureInfo.name}</title>
</svelte:head>

<ServiceCard {service} />
