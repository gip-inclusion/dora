<script lang="ts">
  import { copyIcon2 } from "$lib/icons";

  interface Props {
    warning?: boolean;
    small?: boolean;
  }

  let { warning = false, small = false }: Props = $props();
</script>

<div
  class="bg-service-blue p-s8 text-service-blue-dark rounded-full"
  class:small
  class:warning
>
  <div class="h-s16 w-s16 fill-current">
    {@html copyIcon2}
  </div>
</div>

<style lang="postcss">
  @reference "../../../../app.css";

  .warning {
    @apply bg-service-orange-darker text-white;
  }
  .small {
    @apply p-s6;
  }
</style>
