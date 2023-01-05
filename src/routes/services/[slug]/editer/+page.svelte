<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import NoticePublication from "./notice-publication.svelte";
  import ServiceFields from "../../service-edition-form.svelte";
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
