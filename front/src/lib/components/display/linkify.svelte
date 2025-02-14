<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { externalLinkIcon } from "$lib/icons";

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
      class="text-magenta-cta underline"
      >{part.display}{#if part.value.startsWith("http")}
        <span class="h-s20 w-s20 pl-s4 pt-s6 inline-block fill-current"
          >{@html externalLinkIcon}</span
        >{/if}</a
    >
  {:else}
    {part.value}
  {/if}
{/each}
