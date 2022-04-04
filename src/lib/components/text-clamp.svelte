<script>
  import Button from "./button.svelte";

  export let text = "";
  export let maxLen = 60;

  function shorten(str, separator = " ") {
    return `${str.split(" ").splice(0, maxLen).join(separator)}…`;
  }

  let showAll = false;
  let label;

  function toggle() {
    showAll = !showAll;
  }

  let textVisible, textIsTooLong;

  $: textIsTooLong = text.split(" ").length > maxLen;
  $: textVisible = showAll || !textIsTooLong ? text : shorten(text);
  $: label = showAll ? "réduire" : "Lire la suite";
</script>

<p class="prose mb-s24">{@html textVisible}</p>

{#if textIsTooLong}
  <Button {label} on:click={toggle} noBackground small noPadding />
{/if}
