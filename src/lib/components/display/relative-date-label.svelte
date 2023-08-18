<script lang="ts" context="module">
  import dayjs from "dayjs";

  export function computeRelativeDateLabel(dateString: string) {
    const day = dayjs(dateString);
    const dayDiff = dayjs().diff(day, "day");
    const weekDiff = dayjs().diff(day, "week");
    const monthDiff = dayjs().diff(day, "month");
    const yearDiff = dayjs().diff(day, "year");

    let label = "";
    if (dayDiff < 1) {
      label = `aujourd’hui`;
    } else if (dayDiff < 7) {
      label = `il y a ${dayDiff} jour${dayDiff > 1 ? "s" : ""}`;
    } else if (weekDiff <= 5) {
      label = `il y a ${weekDiff} semaine${weekDiff > 1 ? "s" : ""}`;
    } else if (monthDiff < 12) {
      label = `il y a ${monthDiff} mois`;
    } else {
      label = `il y a plus de ${yearDiff} an${yearDiff > 1 ? "s" : ""}`;
    }
    return label;
  }
</script>

<script lang="ts">
  import DateLabel from "./date-label.svelte";

  export let date;
  export let bold = false;
  export let prefix = "";
</script>

<span class="hidden print:inline" class:font-bold={bold}>
  {prefix ? `${prefix} ` : ""}<DateLabel {date} />
</span>
<span class="print:hidden" class:font-bold={bold}>
  {prefix ? `${prefix} ` : ""}{computeRelativeDateLabel(date)}
</span>
