<script>
  import Label from "$lib/components/label.svelte";
  import { mapPinIcon } from "$lib/icons";

  export let structure, currentTab;
</script>

<style lang="postcss">
  .tab {
    @apply bg-magenta-dark text-white text-f16 font-bold px-s20 py-s12 rounded-t mr-s8 cursor-pointer;
  }

  .tab.active {
    @apply bg-white text-france-blue;
  }
</style>

<h1 class="text-white mb-s24">{structure.name}</h1>

<Label
  label={`${structure.address1}${
    structure.address2 ? `, ${structure.address2}` : ""
  }, ${structure.postalCode} ${structure.city}`}
  iconOnLeft
  icon={mapPinIcon}
  darkBg
  smallIcon
/>
<div class="mb-s48" />

<div class="flex flex-row md:ml-s24">
  <a
    class="tab"
    class:active={currentTab === 1}
    sveltekit:noscroll
    href="/structures/{structure.slug}"
  >
    La structure
  </a>
  <a
    class="tab"
    class:active={currentTab === 2}
    sveltekit:noscroll
    href="/structures/{structure.slug}/services"
  >
    Les services
  </a>
</div>
