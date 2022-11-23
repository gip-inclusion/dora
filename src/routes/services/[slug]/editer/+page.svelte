<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

  let { service, servicesOptions, structures, structure, model } = data;
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import NoticePublication from "$lib/components/services/form/notice-publication.svelte";
  import ServiceFields from "$lib/components/services/form/service-fields.svelte";
</script>

<svelte:head>
  <title>Éditer | {service?.name} | {structure?.name} | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Modification du service</h1>
    <NoticePublication {service} {servicesOptions} />
  </CenteredGrid>

  <ServiceFields {service} {servicesOptions} {structures} {structure} {model} />
</EnsureLoggedIn>
