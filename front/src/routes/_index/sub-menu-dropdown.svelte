<script lang="ts">
  // Dropdown avec le design issu du header du DSFR
  // => https://www.systeme-de-design.gouv.fr/elements-d-interface/composants/en-tete/
  import { afterNavigate } from "$app/navigation";
  import { page } from "$app/stores";
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
  import { clickOutside } from "$lib/utils/misc";
  import { randomId } from "$lib/utils/random";

  export let mobileDesign = false;
  export let buttonClass = mobileDesign
    ? "py-s16 text-f18 font-bold text-gray-dark w-full flex justify-between"
    : "text-f14 text-gray-text p-s16";

  export let label: string;
  export let links: { href: string; label: string; openInNewTab?: boolean }[] =
    [];
  let isOpen = false;
  let dropdownButton;
  const id = `sub-dropdown-menu-${randomId()}`;

  function handleClickOutside(_event) {
    isOpen = false;
  }

  function onKeyDown(event) {
    if (event.key === "Escape") {
      isOpen = false;
      dropdownButton.focus();
    }
  }

  afterNavigate(() => {
    isOpen = false;
  });
</script>

<div
  class="relative {mobileDesign ? 'border-gray-03 border-b' : ''}"
  use:clickOutside
  role="presentation"
  on:click_outside={handleClickOutside}
  on:keydown={onKeyDown}
>
  <button
    bind:this={dropdownButton}
    aria-expanded={isOpen}
    aria-controls={id}
    class:bg-magenta-10={isOpen}
    class="hover:bg-magenta-10 flex h-full items-center {buttonClass}"
    on:click={() => (isOpen = !isOpen)}
  >
    <span>{label}</span>
    <span
      class="ml-s8 h-s24 w-s24 inline-block fill-current {isOpen
        ? 'text-magenta-cta'
        : 'text-gray-text'}"
    >
      {#if isOpen}
        {@html arrowUpSIcon}
      {:else}
        {@html arrowDownSIcon}
      {/if}
    </span>
  </button>

  <ul
    {id}
    class="{mobileDesign ? '' : 'top-[100%)] absolute'} z-10 bg-white"
    class:hidden={!isOpen}
  >
    {#each links as { href, label: linkLabel, openInNewTab }, index}
      {@const currentPage = $page.url.pathname === href}
      <li class="text-f14 hover:bg-magenta-10 whitespace-nowrap">
        <a
          {href}
          class="py-s16 pl-s16 pr-s32 inline-block w-full
          {currentPage
            ? 'border-magenta-cta text-magenta-cta'
            : 'border-gray-03 text-gray-text'}
          {index === links.length - 1 || mobileDesign
            ? 'border-b-none'
            : 'border-b'}"
          target={openInNewTab ? "_blank" : undefined}
          rel={openInNewTab ? "noopener noreferrer" : undefined}
        >
          {linkLabel}
        </a>
      </li>
    {/each}
  </ul>
</div>
