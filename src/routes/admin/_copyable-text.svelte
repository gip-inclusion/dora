<script>
  export let text;
</script>

<span
  class="cursor-pointer text-f10 text-gray-text-alt underline"
  on:click={() => {
    navigator.clipboard.writeText(text);
  }}>copier</span
>
