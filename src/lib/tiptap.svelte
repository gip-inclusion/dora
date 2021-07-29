<script>
  import { onMount, onDestroy } from "svelte";
  import { Editor } from "@tiptap/core";
  import StarterKit from "@tiptap/starter-kit";

  import {
    boldIcon,
    italicIcon,
    paraIcon,
    h1Icon,
    h2Icon,
    liIcon,
  } from "$lib/icons.js";

  let element;
  let editor;
  export let className;
  export let htmlContent = "";
  export let initialContent = "";

  onMount(() => {
    editor = new Editor({
      element: element,
      extensions: [StarterKit],
      content: initialContent,
      injectCSS: false,
      onTransaction: () => {
        // force re-render so `editor.isActive` works as expected
        htmlContent = editor.getHTML();
        editor = editor;
      },
      editorProps: {
        attributes: {
          class: className,
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

<style>
  .tb-button {
    @apply h-6 w-6;
  }
  .active {
    @apply bg-gray-02;
  }
</style>

<div class="flex flex-col w-full">
  {#if editor}
    <div class="flex flex-row">
      <button
        on:click={() => editor.chain().focus().toggleBold().run()}
        class:active={editor.isActive("bold")}
        class="tb-button">
        {@html boldIcon}
      </button>
      <button
        on:click={() => editor.chain().focus().toggleItalic().run()}
        class:active={editor.isActive("italic")}
        class="tb-button">
        {@html italicIcon}
      </button>

      <button
        on:click={() => editor.chain().focus().setParagraph().run()}
        class:active={editor.isActive("paragraph")}
        class="tb-button">
        {@html paraIcon}
      </button>
      <button
        on:click={() =>
          editor.chain().focus().toggleHeading({ level: 2 }).run()}
        class:active={editor.isActive("heading", { level: 2 })}
        class="tb-button">
        {@html h1Icon}
      </button>
      <button
        on:click={() =>
          editor.chain().focus().toggleHeading({ level: 3 }).run()}
        class:active={editor.isActive("heading", { level: 3 })}
        class="tb-button">
        {@html h2Icon}
      </button>
      <button
        on:click={() => editor.chain().focus().toggleBulletList().run()}
        class:active={editor.isActive("bulletList")}
        class="tb-button">
        {@html liIcon}
      </button>
    </div>
  {/if}
  <div>
    <div bind:this={element} />
  </div>
</div>
