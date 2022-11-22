<script lang="ts">
  export let date;
</script>

{new Date(date).toLocaleDateString("fr-FR", {
  year: "numeric",
  month: "long",
  day: "numeric",
})}
