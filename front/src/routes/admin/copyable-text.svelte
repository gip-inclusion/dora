<script lang="ts">
  interface Props {
    text: string;
  }

  let { text }: Props = $props();
</script>

<span
  class="text-f10 text-gray-text-alt cursor-pointer underline"
  tabindex="0"
  role="button"
  onkeypress={(event) => {
    if (event.code === "Enter") {
      navigator.clipboard.writeText(text);
    }
  }}
  onclick={() => {
    navigator.clipboard.writeText(text);
  }}>copier</span
>
