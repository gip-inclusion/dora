<script lang="ts">
  export let label = "";
  export let bold = false;
  export let italic = false;
  export let info = false;
  export let success = false;
  export let error = false;
  export let wait = false;
  export let light = false;
  export let icon: string | null = null;
  export let smallIcon = false;
  export let truncate = false;
</script>

<div
  class="text-f14 flex flex-row items-center"
  class:bold
  class:italic
  class:success
  class:error
  class:info
  class:wait
  class:light
>
  {#if icon}
    <i class="icon flex-none" class:small-icon={smallIcon} class:mr-s8={label}>
      {@html icon}
    </i>
  {/if}

  {#if label || $$slots.default}
    <span class:truncate><slot>{label}</slot></span>
  {/if}
</div>

<style lang="postcss">
  @reference "../../../app.css";

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

  .icon {
    width: var(--spacing-s24);
    height: var(--spacing-s24);
    fill: currentColor;
  }

  .small-icon {
    width: var(--spacing-s16);
    height: var(--spacing-s16);
    fill: currentColor;
  }
</style>
