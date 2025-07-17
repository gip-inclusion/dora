<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import ExternalLinkIcon from "./external-link-icon.svelte";

  interface Props {
    text: string;
  }

  let { text }: Props = $props();

  type Parts = Array<
    | { type: "link"; value: string; display: string; key: number }
    | { type: "text"; value: string; key: number }
  >;

  const dispatch = createEventDispatcher<{ linkClick: { url: string } }>();

  function linkify(string: string) {
    const urlRegex = /(https?:\/\/[^\s]+|mailto:[^\s]+|tel:[^\s]+)/g;
    return string.split(urlRegex).map((part, index) => {
      if (urlRegex.test(part)) {
        const matches = part.match(urlRegex);
        if (matches) {
          const match = matches[0];
          if (match.startsWith("mailto:")) {
            const email = match.replace("mailto:", "");
            return { type: "link", value: match, display: email, key: index };
          } else if (match.startsWith("tel:")) {
            const phone = match.replace("tel:", "");
            return { type: "link", value: match, display: phone, key: index };
          }
          return { type: "link", value: match, display: match, key: index };
        }
      }
      return { type: "text", value: part, key: index };
    }) as Parts;
  }

  function handleLinkClick(url: string) {
    dispatch("linkClick", { url });
  }

  let parts = $derived(linkify(text));
</script>

{#each parts as part}
  {#if part.type === "link"}
    <a
      href={part.value}
      onclick={() => handleLinkClick(part.value)}
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
