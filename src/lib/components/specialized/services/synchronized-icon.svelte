<script lang="ts">
  import { copyIcon2 } from "$lib/icons";

  export let warning = false;
  export let small = false;
</script>

<div
  class="rounded-full bg-service-blue p-s8 text-service-blue-dark"
  class:small
  class:warning
>
  <div class="h-s16 w-s16 fill-current">
    {@html copyIcon2}
  </div>
</div>

<style lang="postcss">
  .warning {
    @apply bg-service-orange-darker text-white;
  }
  .small {
    @apply p-s6;
  }
</style>
