<script>
  export let label = "";
  export let bold = false;
  export let italic = false;
  export let success = false;
  export let error = false;
  export let wait = false;
  export let icon = null;
  export let iconOnLeft = false,
    iconOnRight = false;
  export let darkBg = false;
  export let bigIcon = false;
  export let smallIcon = false;
</script>

<style>
  .wrapper {
    color: var(--col-text);
  }

  .success {
    color: var(--col-success);
  }

  .error {
    color: var(--col-error);
  }

  .wait {
    color: var(--col-wait);
  }

  .bold {
    font-weight: bold;
  }

  .italic {
    font-style: italic;
  }

  .dark-bg {
    color: var(--col-white);
  }

  .dark-bg.success {
    color: var(--col-available-dark);
  }

  .icon {
    width: var(--s24);
    height: var(--s24);
    fill: currentColor;
  }

  .big-icon {
    width: var(--s32);
    height: var(--s32);
  }

  .small-icon {
    width: var(--s16);
    height: var(--s16);
    fill: currentColor;
  }
</style>

<div
  class="wrapper text-sm leading-normal flex flex-row items-center"
  class:bold
  class:italic
  class:success
  class:error
  class:wait
  class:dark-bg={darkBg}>
  {#if iconOnLeft}
    <div
      class="icon mr-1"
      class:big-icon={bigIcon}
      class:small-icon={smallIcon}>
      {@html icon}
    </div>
  {/if}
  {#if icon && !(label || $$slots.default)}
    <div class="icon" class:big-icon={bigIcon}>
      {@html icon}
    </div>
  {/if}

  <slot>{label}</slot>
  {#if iconOnRight}
    <div class="icon ml-1" class:big-icon={bigIcon}>
      {@html icon}
    </div>
  {/if}
</div>
