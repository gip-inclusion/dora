<script lang="ts">
  export let label = "";
  export let otherTab = false;
  export let disabled = false;
  export let href;
  export let nofollow = false;
</script>

<a
  class="text-f14 text-gray-text-alt2"
  on:click
  {href}
  target={otherTab ? "_blank" : ""}
  rel="noopener {nofollow ? 'nofollow' : ''}"
  {disabled}
>
  {label}
</a>
