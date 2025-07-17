<script lang="ts">
  import { run } from "svelte/legacy";

  import {
    boldIcon,
    h1Icon,
    h2Icon,
    italicIcon,
    liIcon,
    linkIcon,
    paraIcon,
  } from "$lib/icons";
  import { htmlToMarkdown, markdownToHTML } from "$lib/utils/misc";
  import { Editor } from "@tiptap/core";
  import Link from "@tiptap/extension-link";
  import Placeholder from "@tiptap/extension-placeholder";
  import StarterKit from "@tiptap/starter-kit";
  import { onDestroy, onMount, tick } from "svelte";
  import Button from "./button.svelte";
  import Separator from "./separator.svelte";

  interface Props {
    id: string;
    name: string;
    htmlContent?: string;
    initialContent?: string;
    placeholder?: string;
    disabled?: boolean;
    readonly?: boolean;
    ariaDescribedBy?: string;
  }

  let {
    id,
    name,
    htmlContent = $bindable(""),
    initialContent = "",
    placeholder = "",
    disabled = false,
    readonly = false,
    ariaDescribedBy = "",
  }: Props = $props();

  let element = $state();
  let editor = $state();
  let linkDialogIsOpen = $state(false);
  let linkDialogHref = $state();
  let linkDialogHrefPrev = $state();
  let linkDialogButtontext = $state();
  let linkDialogButtonIsActive = $state(false);
  let linkDialogText = $state();
  let linkDialogHasSelection = $state();
  let linkDialogTextInput = $state();
  let linkDialogUrlInput = $state();

  function toString(bool: boolean) {
    return bool ? "true" : "false";
  }

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
        console.log("onTransaction");
        // force re-render so `editor.isActive` works as expected
        htmlContent = htmlToMarkdown(editor.getHTML());
      },
      editorProps: {
        attributes: {
          id: name,
          name,
          disabled: toString(disabled),
          readonly: toString(readonly),
          class: `prose bg-white p-s16 whitespace-pre-wrap w-full max-w-none overflow-auto focus:outline-hidden min-h-[160px]`,
        },
      },
    });
  });

  onDestroy(() => {
    if (editor) {
      editor.destroy();
    }
  });

  run(() => {
    linkDialogButtonIsActive =
      linkDialogHref !== linkDialogHrefPrev &&
      !(linkDialogHref === "" && linkDialogHrefPrev === undefined) &&
      (linkDialogHasSelection || linkDialogText);
  });

  run(() => {
    if (!linkDialogHrefPrev) {
      linkDialogButtontext = "Ajouter le lien";
    } else if (!linkDialogHref) {
      linkDialogButtontext = "Supprimer le lien";
    } else {
      linkDialogButtontext = "Modifier le lien";
    }
  });

  export function updateValue(value) {
    editor.commands.setContent(markdownToHTML(value));
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

  function linkDialogToggle() {
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

<div class="border-gray-03 flex w-full flex-col border">
  {#if editor}
    <div class="gap-s8 bg-gray-03 p-s12 flex flex-row items-center">
      <Button
        on:click={() => editor.chain().focus().toggleBold().run()}
        active={editor.isActive("bold")}
        icon={boldIcon}
        label="Gras"
      />

      <Button
        on:click={() => editor.chain().focus().toggleItalic().run()}
        active={editor.isActive("italic")}
        icon={italicIcon}
        label="Italique"
      />

      <Separator />

      <Button
        on:click={() => editor.chain().focus().setParagraph().run()}
        active={editor.isActive("paragraph")}
        icon={paraIcon}
        label="Paragraphe"
      />

      <Button
        on:click={() =>
          editor.chain().focus().toggleHeading({ level: 1 }).run()}
        active={editor.isActive("heading", { level: 1 })}
        icon={h1Icon}
        label="Titre de niveau 1"
      />

      <Button
        on:click={() =>
          editor.chain().focus().toggleHeading({ level: 2 }).run()}
        active={editor.isActive("heading", { level: 2 })}
        icon={h2Icon}
        label="Titre de niveau 2"
      />

      <Separator />

      <Button
        on:click={() => editor.chain().focus().toggleBulletList().run()}
        active={editor.isActive("bulletList")}
        icon={liIcon}
        label="Liste à puces"
      />

      <Separator />

      <Button
        on:click={linkDialogToggle}
        active={editor.isActive("link")}
        icon={linkIcon}
        label="Lien"
      />
    </div>
  {/if}
  <div class="relative">
    {#if linkDialogIsOpen}
      <div class="inset-x-s0 gap-s12 bg-gray-01 p-s12 absolute flex">
        {#if !linkDialogHasSelection}
          <input
            bind:this={linkDialogTextInput}
            type="text"
            placeholder="lien"
            class="px-s8 py-s4 flex-1"
            bind:value={linkDialogText}
          />
        {/if}
        <input
          bind:this={linkDialogUrlInput}
          type="text"
          placeholder="https://example.com"
          class="px-s8 py-s4 flex-1"
          bind:value={linkDialogHref}
        />
        <button
          class="border-gray-text px-s8 py-s4 text-f12 hover:bg-gray-text disabled:border-gray-03 disabled:bg-gray-01 disabled:text-gray-03 rounded-lg border font-bold hover:text-white"
          onclick={setLink}
          disabled={!linkDialogButtonIsActive}
        >
          {linkDialogButtontext}
        </button>
        <button
          class="border-gray-text px-s8 py-s4 text-f12 hover:bg-gray-text rounded-lg border font-bold hover:text-white"
          onclick={linkDialogClose}>Annuler</button
        >
      </div>
    {/if}
    <div {id} aria-describedby={ariaDescribedBy} bind:this={element}></div>
  </div>
</div>

<style lang="postcss">
  @reference "../../../../app.css";

  :global(.ProseMirror p.is-editor-empty:first-child::before) {
    content: attr(data-placeholder);

    @apply h-s0 text-gray-text-alt2 pointer-events-none float-left;
  }
</style>
