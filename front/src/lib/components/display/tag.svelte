<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    variant?: "default" | "success" | "info";
    children: Snippet;
  }

  let { variant = "default", children }: Props = $props();

  const variantClasses = {
    default: "bg-gray-text-alt text-white",
    success: "bg-success text-white",
    info: "bg-blue-information text-gray-text",
  };
</script>

<span
  class={[
    "break-word px-s8 py-s2 text-f12 rounded-sm font-bold uppercase",
    variantClasses[variant],
  ]}
>
  {@render children()}
</span>
