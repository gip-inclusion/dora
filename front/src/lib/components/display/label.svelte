<script lang="ts">
  interface Props {
    label?: string;
    bold?: boolean;
    italic?: boolean;
    info?: boolean;
    success?: boolean;
    error?: boolean;
    wait?: boolean;
    light?: boolean;
    icon?: string | null;
    darkBg?: boolean;
    smallIcon?: boolean;
    truncate?: boolean;
    children?: import('svelte').Snippet;
  }

  let {
    label = "",
    bold = false,
    italic = false,
    info = false,
    success = false,
    error = false,
    wait = false,
    light = false,
    icon = null,
    darkBg = false,
    smallIcon = false,
    truncate = false,
    children
  }: Props = $props();
</script>

<div
  class="text-f14 flex flex-row items-center {darkBg
    ? 'print:text-gray-text text-white'
    : ''}"
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

  {#if label || children}
    <span class:truncate>{#if children}{@render children()}{:else}{label}{/if}</span>
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
