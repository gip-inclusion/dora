<script lang="ts">
  export let text;
</script>

<span
  class="text-f10 text-gray-text-alt cursor-pointer underline"
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
