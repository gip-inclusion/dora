<script>
  import { onMount, onDestroy } from "svelte";
  import { Editor } from "@tiptap/core";
  import StarterKit from "@tiptap/starter-kit";
  import Placeholder from "@tiptap/extension-placeholder";

  import {
    boldIcon,
    italicIcon,
    paraIcon,
    h1Icon,
    h2Icon,
    liIcon,
  } from "$lib/icons.js";

  import Button from "./button.svelte";
  import Separator from "./separator.svelte";

  let element;
  let editor;
  export let name;
  export let className = "prose bg-white h-s160";
  export let htmlContent = "";
  export let initialContent = "";
  export let placeholder = "";
  export let disabled = false;
  export let readonly;

  onMount(() => {
    editor = new Editor({
      element,
      extensions: [StarterKit, Placeholder.configure({ placeholder })],
      content: initialContent,
      injectCSS: false,
      onTransaction: () => {
        // force re-render so `editor.isActive` works as expected
        htmlContent = editor.getHTML();
        editor = editor;
      },
      editorProps: {
        attributes: {
          id: { name },
          name,
          disabled,
          readonly,
          class: `${className} p-s16 whitespace-pre-wrap w-full max-w-none overflow-auto focus:outline-none`,
        },
      },
    });
  });

  onDestroy(() => {
    if (editor) {
      editor.destroy();
    }
  });
</script>

<style lang="postcss">
  :global(.ProseMirror p.is-editor-empty:first-child::before) {
    content: attr(data-placeholder);

    @apply text-gray-text-alt pointer-events-none h-s0 float-left;
  }
</style>

<div class="flex flex-col w-full border border-gray-03">
  {#if editor}
    <div class="flex flex-row items-center bg-gray-03 p-s12 ">
      <Button
        on:click={() => editor.chain().focus().toggleBold().run()}
        active={editor.isActive("bold")}
        icon={boldIcon}
      />

      <Button
        on:click={() => editor.chain().focus().toggleItalic().run()}
        active={editor.isActive("italic")}
        icon={italicIcon}
      />

      <Separator />

      <Button
        on:click={() => editor.chain().focus().setParagraph().run()}
        active={editor.isActive("paragraph")}
        icon={paraIcon}
      />

      <Button
        on:click={() =>
          editor.chain().focus().toggleHeading({ level: 2 }).run()}
        active={editor.isActive("heading", { level: 2 })}
        icon={h1Icon}
      />

      <Button
        on:click={() =>
          editor.chain().focus().toggleHeading({ level: 3 }).run()}
        active={editor.isActive("heading", { level: 3 })}
        icon={h2Icon}
      />

      <Separator />

      <Button
        on:click={() => editor.chain().focus().toggleBulletList().run()}
        active={editor.isActive("bulletList")}
        icon={liIcon}
      />

      <Separator />
    </div>
  {/if}
  <div>
    <div bind:this={element} />
  </div>
</div>
