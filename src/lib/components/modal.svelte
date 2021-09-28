<script>
  export let isOpen;
  $: display = isOpen ? "block" : "none";
</script>

<style>
  #background {
    position: fixed;
    z-index: 1;
    top: 0;
    left: 0;
    display: var(--display);
    width: 100vw;
    height: 100vh;
    background-color: black;
    opacity: 0.5;
  }

  #modal {
    position: fixed;
    z-index: 1;
    top: 50%;
    left: 50%;
    display: var(--display);
    transform: translate(-50%, -50%);
  }
</style>

<div
  id="background"
  style="--display: {display};"
  on:click={() => (isOpen = false)} />
<div id="modal" style="--display: {display};">
  <slot />
</div>
