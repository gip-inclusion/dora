<script lang="ts">
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import NoticePublication from "$lib/components/services/form/notice-publication.svelte";
  import ServiceFields from "$lib/components/services/form/service-fields.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Modification du service</h1>
    <NoticePublication
      service={data.service}
      servicesOptions={data.servicesOptions}
    />
  </CenteredGrid>

  <ServiceFields
    service={data.service}
    servicesOptions={data.servicesOptions}
    structures={data.structures}
    structure={data.structure}
    model={data.model}
  />
</EnsureLoggedIn>
