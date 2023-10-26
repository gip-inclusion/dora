<script lang="ts">
  export let text;
</script>

<span
  class="cursor-pointer text-f10 text-gray-text-alt underline"
  tabindex="0"
  role="button"
  on:keypress={(event) => {
    if (event.code === "Enter") {
      navigator.clipboard.writeText(text);
    }
  }}
  on:click={() => {
    navigator.clipboard.writeText(text);
  }}>copier</span
>
