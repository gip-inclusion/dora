<script lang="ts">
  import { errorWarningLineIcon, historyLineIcon } from "$lib/icons";

  interface Props {
    small?: boolean;
    updateNeeded: boolean;
  }

  let { small = false, updateNeeded }: Props = $props();

  const textColor = updateNeeded ? "text-white" : "text-service-blue-dark";
  const icon = updateNeeded ? errorWarningLineIcon : historyLineIcon;
  const iconBg = updateNeeded ? "bg-wait-dark" : "bg-service-blue";
</script>

<div class="p-s12 container rounded-full {iconBg}" class:small>
  <div class="icon h-s24 w-s24 fill-current {textColor}" class:small>
    {@html icon}
  </div>
</div>

<style lang="postcss">
  @reference "../../../../app.css";

  .container.small {
    @apply p-s6;
  }
  .icon.small {
    @apply h-s16 w-s16;
  }
</style>
