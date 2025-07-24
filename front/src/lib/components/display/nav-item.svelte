<script lang="ts">
  interface Props {
    label?: string;
    otherTab?: boolean;
    disabled?: boolean;
    href: any;
    onclick?: () => void;
  }

  let {
    label = "",
    otherTab = false,
    disabled = false,
    href,
    onclick,
  }: Props = $props();
</script>

<a
  class="text-f14 text-gray-text"
  {onclick}
  {href}
  target={otherTab ? "_blank" : ""}
  rel="noopener"
  {disabled}
>
  {label}
</a>
