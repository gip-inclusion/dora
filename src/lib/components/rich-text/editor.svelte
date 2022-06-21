<script>
  import { onMount, onDestroy, tick } from "svelte";
  import { Editor } from "@tiptap/core";
  import StarterKit from "@tiptap/starter-kit";
  import Placeholder from "@tiptap/extension-placeholder";
  import Link from "@tiptap/extension-link";

  import {
    boldIcon,
    italicIcon,
    paraIcon,
    h1Icon,
    h2Icon,
    liIcon,
    linkIcon,
  } from "$lib/icons.js";

  import Button from "./button.svelte";
  import Separator from "./separator.svelte";
  import { htmlToMarkdown, markdownToHTML } from "$lib/utils";

  export let name;
  export let htmlContent = "";
  export let initialContent = "";
  export let placeholder = "";
  export let disabled = false;
  export let readonly;

  let element;
  let editor;
  let linkDialogIsOpen = false;
  let linkDialogHref;
  let linkDialogHrefPrev;
  let linkDialogButtontext;
  let linkDialogButtonIsActive = false;
  let linkDialogText;
  let linkDialogHasSelection;
  let linkDialogTextInput;
  let linkDialogUrlInput;

  onMount(() => {
    editor = new Editor({
      element,
      extensions: [
        StarterKit,
        Placeholder.configure({ placeholder }),
        Link.configure({
          HTMLAttributes: { class: "underline" },
          openOnClick: false,
        }),
      ],
      content: markdownToHTML(initialContent),
      injectCSS: false,
      onTransaction: () => {
        // force re-render so `editor.isActive` works as expected
        htmlContent = htmlToMarkdown(editor.getHTML());
        editor = editor;
      },
      editorProps: {
        attributes: {
          id: { name },
          name,
          disabled,
          readonly,
          class: `prose bg-white p-s16 whitespace-pre-wrap w-full max-w-none overflow-auto focus:outline-none`,
        },
      },
    });
  });

  onDestroy(() => {
    if (editor) {
      editor.destroy();
    }
  });

  $: linkDialogButtonIsActive =
    linkDialogHref !== linkDialogHrefPrev &&
    !(linkDialogHref === "" && linkDialogHrefPrev === undefined) &&
    (linkDialogHasSelection || linkDialogText);

  $: {
    if (!linkDialogHrefPrev) {
      linkDialogButtontext = "Ajouter le lien";
    } else if (!linkDialogHref) {
      linkDialogButtontext = "Supprimer le lien";
    } else {
      linkDialogButtontext = "Modifier le lien";
    }
  }

  export function updateValue(v) {
    editor.commands.setContent(markdownToHTML(v));
  }

  async function linkDialogOpen() {
    linkDialogHref = linkDialogHrefPrev = editor.getAttributes("link").href;
    linkDialogHasSelection = !editor.state.selection.empty;
    linkDialogIsOpen = true;

    await tick();

    if (linkDialogHasSelection) {
      linkDialogUrlInput.focus();
    } else {
      linkDialogTextInput.focus();
    }
  }

  function linkDialogClose() {
    linkDialogIsOpen = false;
  }

  async function linkDialogToggle() {
    if (linkDialogIsOpen) {
      linkDialogClose();
    } else {
      linkDialogOpen();
    }
  }

  function setLink() {
    if (linkDialogHref === "") {
      editor.chain().focus().extendMarkRange("link").unsetLink().run();
    } else if (!editor.state.selection.empty) {
      editor
        .chain()
        .focus()
        .extendMarkRange("link")
        .setLink({ href: linkDialogHref })
        .run();
    } else {
      editor
        .chain()
        .focus()
        .insertContent(` ${linkDialogText}`)
        .setTextSelection({
          from: editor.state.selection.from + 1,
          to: editor.state.selection.from + 1 + linkDialogText.length,
        })
        .extendMarkRange("link")
        .setLink({ href: linkDialogHref })
        .run();
    }

    linkDialogIsOpen = false;
  }
</script>

<div class="flex w-full flex-col border border-gray-03">
  {#if editor}
    <div class="flex flex-row items-center gap-s8 bg-gray-03 p-s12">
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

      <Button
        on:click={linkDialogToggle}
        active={editor.isActive("link")}
        icon={linkIcon}
      />
    </div>
  {/if}
  <div class="relative">
    {#if linkDialogIsOpen}
      <div class="absolute inset-x-s0 flex gap-s12 bg-gray-01 p-s12">
        {#if !linkDialogHasSelection}
          <input
            bind:this={linkDialogTextInput}
            type="text"
            placeholder="lien"
            class="flex-1 py-s4 px-s8"
            bind:value={linkDialogText}
          />
        {/if}
        <input
          bind:this={linkDialogUrlInput}
          type="text"
          placeholder="http://example.com"
          class="flex-1 py-s4 px-s8"
          bind:value={linkDialogHref}
        />
        <button
          class="text-grayborder-gray-text rounded-md border border-gray-text py-s4 px-s8 text-f12 font-bold hover:bg-gray-text hover:text-white disabled:border-gray-03 disabled:bg-gray-01 disabled:text-gray-03"
          on:click={setLink}
          disabled={!linkDialogButtonIsActive}
        >
          {linkDialogButtontext}
        </button>
        <button
          class="text-grayborder-gray-text rounded-md border border-gray-text py-s4 px-s8 text-f12 font-bold hover:bg-gray-text hover:text-white"
          on:click={linkDialogClose}>Annuler</button
        >
      </div>
    {/if}
    <div bind:this={element} />
  </div>
</div>

<style lang="postcss">
  :global(.ProseMirror p.is-editor-empty:first-child::before) {
    content: attr(data-placeholder);

    @apply pointer-events-none float-left h-s0 text-gray-text-alt;
  }
</style>
