<script lang="ts">
  interface Props {
    resultCount: number;
    cityLabel: string;
  }

  let { resultCount, cityLabel }: Props = $props();
</script>

<span
  >{resultCount > 0 ? resultCount : "Aucun"}
  {resultCount > 1 ? "services" : "service"}
  à proximité de <b>{cityLabel}</b></span
>
