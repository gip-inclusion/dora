<script lang="ts">
  export let label = "";
  export let otherTab = false;
  export let disabled = false;
  export let href;
</script>

<a
  class="text-f14 text-gray-text"
  on:click
  {href}
  target={otherTab ? "_blank" : ""}
  rel="noopener"
  {disabled}
>
  {label}
</a>
