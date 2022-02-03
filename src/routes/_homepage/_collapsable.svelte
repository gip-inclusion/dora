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

<div class="wrapper flex justify-between" bind:this={wrapper}>
  <slot name="above-fold" />
  <div
    class="ml-s8 h-s24 w-s24 fill-current text-magenta-cta"
    on:click={handleToggleFold}
  >
    {@html folded ? arrowDownSIcon : arrowUpSIcon}
  </div>
</div>
<div class:hidden={folded}>
  <slot name="under-fold" />
</div>

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
