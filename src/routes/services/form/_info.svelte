<script>
  import { informationIcon } from "$lib/icons.js";
  export let title;
  export let icon;
</script>

<style>
  .wrapper {
    padding: var(--s16);
    margin: var(--s32) 0;
    background-color: var(--col-info-light);
    border-radius: var(--s4);
  }

  .title {
    display: flex;
    align-items: center;
    margin-bottom: var(--s8);
    color: var(--col-info);
    font-size: var(--f17);
    font-weight: bold;
  }

  .icon {
    width: var(--s24);
    height: var(--s24);
    margin-right: var(--s8);
    fill: currentColor;
  }

  .text {
    color: var(--col-text);
    font-size: var(--f14);
    line-height: var(--s24);
  }
</style>

<div class="wrapper ">
  {#if title}
    <div class="title">
      <div class="icon">
        {@html icon || informationIcon}
      </div>
      {title}
    </div>
  {/if}
  <div class="text">
    <slot />
  </div>
</div>
