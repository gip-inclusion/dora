<script lang="ts">
  import ExternalLinkIcon from "./external-link-icon.svelte";

  interface Props {
    text: string;
    onLinkClick?: (url: string) => void;
  }

  let { text, onLinkClick }: Props = $props();

  type Parts = Array<
    | { type: "link"; value: string; display: string; key: number }
    | { type: "text"; value: string; key: number }
  >;

  function linkify(string: string) {
    const urlRegex = /(https?:\/\/[^\s]+|mailto:[^\s]+|tel:[^\s]+)/g;
    return string.split(urlRegex).map((part, index) => {
      if (part.startsWith("mailto:")) {
        const email = part.replace("mailto:", "");
        return { type: "link", value: part, display: email, key: index };
      }
      if (part.startsWith("tel:")) {
        const phone = part.replace("tel:", "");
        return { type: "link", value: part, display: phone, key: index };
      }
      if (part.startsWith("http://") || part.startsWith("https://")) {
        return { type: "link", value: part, display: part, key: index };
      }
      return { type: "text", value: part, key: index };
    }) as Parts;
  }

  let parts = $derived(linkify(text));
</script>

{#each parts as part (part.key)}
  {#if part.type === "link"}
    <a
      href={part.value}
      onclick={() => onLinkClick?.(part.value)}
      target="_blank"
      rel="noopener ugc"
      class="underline"
      >{part.display}{#if part.value.startsWith("http")}<ExternalLinkIcon
        />{/if}</a
    >
  {:else}
    {part.value}
  {/if}
{/each}
