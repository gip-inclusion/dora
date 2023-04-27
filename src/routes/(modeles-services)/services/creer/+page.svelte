<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import ServiceEditionForm from "../service-edition-form.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Création d'un service</h1>

    {#if !data.structures.length}
      <Notice title="Impossible de créer un nouveau service" type="error">
        <p class="text-f14">Vous n’êtes rattaché à aucune structure.</p>
      </Notice>
    {/if}
  </CenteredGrid>

  <ServiceEditionForm
    service={data.service}
    servicesOptions={data.servicesOptions}
    structures={data.structures}
    structure={data.structure}
    model={data.model}
  />
</EnsureLoggedIn>
