<script lang="ts">
  import { createBubbler } from "svelte/legacy";

  const bubble = createBubbler();
  interface Props {
    label?: string;
    otherTab?: boolean;
    disabled?: boolean;
    href: any;
  }

  let {
    label = "",
    otherTab = false,
    disabled = false,
    href,
  }: Props = $props();
</script>

<a
  class="text-f14 text-gray-text"
  onclick={bubble("click")}
  {href}
  target={otherTab ? "_blank" : ""}
  rel="noopener"
  {disabled}
>
  {label}
</a>
