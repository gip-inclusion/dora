<script>
  export let label = "";
  export let bold = false;
  export let italic = false;
  export let success = false;
  export let icon = null;
  export let iconOnLeft = false,
    iconOnRight = false;
  export let darkBg = false;
</script>

<style>
  .wrapper {
    color: var(--col-text);
  }

  .success {
    color: var(--col-success);
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
</style>

<div
  class="wrapper text-sm leading-normal flex flex-row items-center"
  class:bold
  class:italic
  class:success
  class:dark-bg={darkBg}>
  {#if iconOnLeft}
    <div class="w-3 h-3 mr-1 fill-current ">
      {@html icon}
    </div>
  {/if}
  {#if icon && !label}
    <div class="w-3 h-3 fill-current">
      {@html icon}
    </div>
  {/if}
  {label}
  {#if iconOnRight}
    <div class="w-3 h-3 ml-1 fill-current">
      {@html icon}
    </div>
  {/if}
</div>
