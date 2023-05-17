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
  export let links: { href: string; label: string }[] = [];
  let isOpen = false;

  const id = `sub-dropdown-menu-${randomId()}`;

  function handleClickOutside(_event) {
    isOpen = false;
  }

  afterNavigate(() => {
    isOpen = false;
  });
</script>

<div
  class="relative {mobileDesign ? 'border-b border-gray-03' : ''}"
  use:clickOutside
  on:click_outside={handleClickOutside}
>
  <button
    aria-expanded={isOpen}
    aria-controls={id}
    class:bg-magenta-10={isOpen}
    class="flex h-full items-center hover:bg-magenta-10 {buttonClass}"
    on:click={() => (isOpen = !isOpen)}
  >
    <span>{label}</span>
    <span
      class="ml-s8 inline-block h-s24 w-s24 fill-current {isOpen
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
    {#each links as link, index}
      {@const currentPage = $page.url.pathname === link.href}
      <li class="whitespace-nowrap pl-s16 text-f14  hover:bg-magenta-10">
        <a
          href={link.href}
          class="inline-block w-full py-s16 pr-s32
          {currentPage
            ? 'border-magenta-cta text-magenta-cta'
            : 'border-gray-03 text-gray-text'}
          {index === links.length - 1 || mobileDesign
            ? 'border-b-none'
            : 'border-b'}"
        >
          {link.label}
        </a>
      </li>
    {/each}
  </ul>
</div>
