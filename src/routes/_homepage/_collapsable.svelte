<script>
  // Inspiration for accessing the breakpoints values from javascript:
  // https://gomakethings.com/the-easy-way-to-manage-css-breakpoints-in-javascript/
  import { onMount } from "svelte";
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";

  let wrapper;
  let folded = true;

  function handleToggleFold() {
    folded = !folded;
  }

  onMount(() => {
    const bp = window
      .getComputedStyle(wrapper, ":before")
      .content.replace(/"/gu, "");
    folded = bp === "xs" || bp === "md";
  });
</script>

<style lang="postcss">
  .wrapper::before {
    display: none;
    content: "xs";
    visibility: hidden;
  }

  @screen md {
    .wrapper::before {
      content: "md";
    }
  }

  @screen lg {
    .wrapper::before {
      content: "lg";
    }
  }

  @screen xl {
    .wrapper::before {
      content: "xl";
    }
  }
</style>

<div class="flex justify-between wrapper" bind:this={wrapper}>
  <slot name="above-fold" />
  <div
    class="w-s24 h-s24 ml-s8 text-magenta-cta fill-current"
    on:click={handleToggleFold}
  >
    {@html folded ? arrowDownSIcon : arrowUpSIcon}
  </div>
</div>
<div class:hidden={folded}>
  <slot name="under-fold" />
</div>
