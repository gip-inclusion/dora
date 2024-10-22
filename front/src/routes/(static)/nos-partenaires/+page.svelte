<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import PartnerList from "$lib/components/specialized/partner-list.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<CenteredGrid>
  <div class="mb-s24">
    <Breadcrumb currentLocation="partners" dark />
  </div>

  <div>
    <h1 class="text-france-blue">Nos partenaires</h1>
    <p>
      Plus de 1 000 structures ont déjà commencé à référencer leurs services sur
      DORA
    </p>

    <ul class="mt-s24 flex w-full flex-wrap justify-center gap-s24">
      <PartnerList imgHeight="medium" partnersToShow={data.partnersToShow} />
    </ul>
  </div>
</CenteredGrid>
