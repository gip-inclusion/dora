<script lang="ts">
  interface Props {
    date: string | number | Date;
  }

  let { date }: Props = $props();
</script>

{new Date(date).toLocaleDateString("fr-FR", {
  year: "numeric",
  month: "long",
  day: "numeric",
})}
