<script>
  import { userInfo } from "$lib/auth";

  import LinkButton from "$lib/components/link-button.svelte";
  import ServiceCard from "$lib/components/services/card.svelte";
  import { addCircleIcon } from "$lib/icons";

  export let structure, services, total;
  export let hasListLink = false;
  export let onRefresh;
  const canEdit = structure.isMember || $userInfo?.isStaff;

  async function handleRefresh() {
    if (onRefresh) {
      onRefresh();
    }
  }
</script>

<div class="col-span-full md:flex md:items-center md:justify-between">
  <h2 class="mb-s24 text-france-blue">Services</h2>
  <div class="flex gap-s16">
    {#if !!services.length && hasListLink}
      <LinkButton
        label={`Voir tous les services (${total})`}
        to="/structures/{structure.slug}/services"
        small
        secondary
      />
    {/if}
  </div>
</div>
<div class="col-span-full">
  <div class="mb-s48 grid gap-s16 md:grid-cols-2 lg:grid-cols-4">
    {#if canEdit}
      <div
        class="flex items-center justify-center rounded-md px-s20 py-s24 shadow-md"
      >
        <LinkButton
          label="Ajouter un service…"
          to="/services/creer"
          icon={addCircleIcon}
          noBackground
        />
      </div>
    {/if}
    {#each services as service}
      <ServiceCard {service} readOnly={!canEdit} onRefresh={handleRefresh} />
    {/each}
  </div>
</div>
