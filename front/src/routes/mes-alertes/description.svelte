<script lang="ts">
  export let search;
</script>

{#if search.subcategories.length || search.kinds.length || search.fees.length}
  <p class="text-f16">
    {#if search.subcategories.length}
      Besoins sélectionnés : {search.subcategoriesDisplay.join(", ")}.
    {:else}
      Aucun besoin sélectionné.
    {/if}

    {#if search.kinds.length}
      Type de services : {search.kindsDisplay.join(", ")}.
    {/if}

    {#if search.fees.length}
      Frais à charge : {search.feesDisplay.join(", ")}.
    {/if}
  </p>
{/if}
