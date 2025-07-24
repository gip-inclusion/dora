<script lang="ts">
  let { date } = $props();
</script>

{new Date(date).toLocaleDateString("fr-FR", {
  year: "numeric",
  month: "long",
  day: "numeric",
})}
