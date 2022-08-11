<script>
  export let condition = true;
</script>

{#if condition}
  <div class="mb-s16 pl-s16">
    <slot />
  </div>
{/if}
