<script lang="ts">
  export let resultCount: number;
  export let cityLabel: string;
</script>

<span
  >{resultCount > 0 ? resultCount : "Aucun"}
  {resultCount > 1 ? "services" : "service"}
  à proximité de <b>{cityLabel}</b></span
>
