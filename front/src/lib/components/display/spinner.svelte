<script lang="ts">
  interface Props {
    size?: string;
    colorClass?: string;
  }

  let { size = "24px", colorClass = "border-magenta-cta" }: Props = $props();
</script>

<div
  class="animate-spin rounded-full border-3 border-t-transparent {colorClass}"
  style:width={size}
  style:height={size}
></div>
