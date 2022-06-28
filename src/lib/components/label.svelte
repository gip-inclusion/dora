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
    <i class="icon flex-none" class:small-icon={smallIcon} class:mr-s8={label}>
      {@html icon}
    </i>
  {/if}

  {#if label}
    <span class:truncate><slot>{label}</slot></span>
  {/if}
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
  }
</style>
