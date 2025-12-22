<script lang="ts">
  import ErrorWarningLineSystem from "svelte-remix/ErrorWarningLineSystem.svelte";
  import HistoryLineSystem from "svelte-remix/HistoryLineSystem.svelte";

  interface Props {
    small?: boolean;
    updateNeeded: boolean;
  }

  let { small = false, updateNeeded }: Props = $props();

  const textColor = updateNeeded ? "text-white" : "text-service-blue-dark";
  const Icon = updateNeeded ? ErrorWarningLineSystem : HistoryLineSystem;
  const iconBg = updateNeeded ? "bg-wait-dark" : "bg-service-blue";
</script>

<div class="p-s12 container rounded-full {iconBg}" class:small>
  <div class="icon h-s24 w-s24 fill-current {textColor}" class:small>
    <Icon />
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
