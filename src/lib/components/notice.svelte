<script>
  export let title;
  export let type = "info";
  import {
    alertLine,
    checkboxCircleLine,
    closeCircleLine,
    informationLine,
  } from "$lib/icons";

  const types = {
    info: {
      bg: "bg-info-light",
      border: "border-info",
      text: "text-info",
      icon: informationLine,
    },
    success: {
      bg: "bg-success-light",
      border: "border-success",
      text: "text-success",
      icon: checkboxCircleLine,
    },
    warning: {
      bg: "bg-warning-light",
      border: "border-warning",
      text: "text-warning",
      icon: alertLine,
    },
    error: {
      bg: "bg-error-light",
      border: "border-error",
      text: "text-error",
      icon: closeCircleLine,
    },
  };
</script>

<div
  class="rounded-r-md border-l-8 {types[type].border} {types[type].bg} p-s24"
>
  <h4 class="mb-s16 {types[type].text} flex">
    <div class="mr-s8 h-s24 w-s24 shrink-0 fill-current">
      {@html types[type].icon}
    </div>
    {title}
  </h4>
  <div class="lg:flex lg:flex-row lg:justify-between lg:gap-s16">
    <slot />

    <div class="self-end">
      <slot name="button" />
    </div>
  </div>
</div>
