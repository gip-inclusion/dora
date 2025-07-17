<script lang="ts">
  let { link, label } = $props();
</script>

<a
  class="text-f10 text-gray-text-alt underline"
  href={link}
  target="_blank"
  rel="noopener"
>
  {label}
</a>
