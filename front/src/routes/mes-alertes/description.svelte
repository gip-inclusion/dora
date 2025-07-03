<script lang="ts">
  let { search } = $props();
</script>

{#if search.subcategories.length || search.kinds.length || search.fees.length || search.fundingLabels.length}
  <p class="text-f16">
    {#if search.subcategories.length}
      Besoins sélectionnés&#8239;: {search.subcategoriesDisplay.join(", ")}.
    {:else}
      Aucun besoin sélectionné.
    {/if}

    {#if search.kinds.length}
      Type de services&#8239;: {search.kindsDisplay.join(", ")}.
    {/if}

    {#if search.fees.length}
      Frais à charge&#8239;: {search.feesDisplay.join(", ")}.
    {/if}

    {#if search.fundingLabels.length}
      Financé par&#8239;: {search.fundingLabelsDisplay.join(", ")}.
    {/if}
  </p>
{/if}
