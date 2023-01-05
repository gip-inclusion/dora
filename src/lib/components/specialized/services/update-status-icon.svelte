<script lang="ts">
  import { alertLine, errorWarningLineIcon, historyLineIcon } from "$lib/icons";
  import type { ServiceUpdateStatus } from "$lib/types";

  export let small = false;
  export let updateStatus: ServiceUpdateStatus;

  type ServiceStatusPresentation = {
    iconBg: string;
    icon: string;
    textColor: string;
  };

  const statusPresentation: Record<
    ServiceUpdateStatus,
    ServiceStatusPresentation
  > = {
    NOT_NEEDED: {
      iconBg: "bg-service-blue",
      icon: historyLineIcon,
      textColor: "text-service-blue-dark",
    },
    NEEDED: {
      iconBg: "bg-wait-dark",
      icon: errorWarningLineIcon,
      textColor: "text-white",
    },
    REQUIRED: {
      iconBg: "bg-service-red-dark",
      icon: alertLine,
      textColor: "text-white",
    },
  };
  const { textColor, icon, iconBg } = statusPresentation[updateStatus];
</script>

<div class="container rounded-full p-s12 {iconBg}" class:small>
  <div class="icon h-s24 w-s24 fill-current  {textColor}" class:small>
    {@html icon}
  </div>
</div>

<style lang="postcss">
  .container.small {
    @apply p-s6;
  }
  .icon.small {
    @apply h-s16 w-s16;
  }
</style>
