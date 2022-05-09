<script>
  export let label = "";
  export let bold = false;
  export let italic = false;
  export let info = false;
  export let success = false;
  export let error = false;
  export let wait = false;
  export let light = false;
  export let icon = null;
  export let darkBg = false;
  export let smallIcon = false;
  export let truncate = false;
</script>

<div
  class="flex flex-row items-center text-f14"
  class:bold
  class:italic
  class:success
  class:error
  class:info
  class:wait
  class:light
  class:dark-bg={darkBg}
>
  {#if icon}
    <div class="icon mr-s8 flex-none" class:small-icon={smallIcon}>
      {@html icon}
    </div>
  {/if}
  {#if icon && !(label || $$slots.default)}
    <div class="icon flex-none">
      {@html icon}
    </div>
  {/if}

  <span class:truncate><slot>{label}</slot></span>
</div>

<style lang="postcss">
  .info {
    color: var(--col-info);
  }

  .light {
    color: var(--col-text-alt);
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

  .small-icon {
    width: var(--s16);
    height: var(--s16);
    fill: currentColor;
  }

  @media print {
    .dark-bg {
      color: var(--col-text);
    }

    .dark-bg.success {
      color: var(--col-success);
    }
  }
</style>
