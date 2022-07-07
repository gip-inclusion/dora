<script>
  import { page } from "$app/stores";
  import Label from "$lib/components/label.svelte";
  import { mapPinIcon } from "$lib/icons";
  import Tabs from "$lib/components/tabs-links.svelte";
  import { userInfo } from "$lib/auth";
  import PendingNotice from "./_pending-notice.svelte";
  import AdminNotice from "$lib/components/structures/admin-notice.svelte";
  import { capitalize } from "$lib/utils";

  export let structure;
  export let tabId = "informations";

  let tabs = [];

  $: {
    tabs = [
      {
        id: "informations",
        name: "Informations",
        href: `/structures/${structure.slug}/`,
      },
    ];

    if (!structure.parent && structure.branches?.length) {
      tabs.splice(1, 0, {
        id: "antennes",
        name: "Antennes",
        href: `/structures/${structure.slug}/antennes`,
      });
    }

    if (
      !!structure.models?.length &&
      (structure.isMember || $userInfo?.isStaff)
    ) {
      tabs.splice(1, 0, {
        id: "modeles",
        name: "Modèles",
        href: `/structures/${structure.slug}/modeles`,
      });
    }

    if (structure.services?.length || structure.archivedServices?.length) {
      tabs.splice(1, 0, {
        id: "services",
        name: "Services",
        href: `/structures/${structure.slug}/services`,
      });
    }
    if (structure.isAdmin || $userInfo?.isStaff || $userInfo?.isBizdev) {
      tabs.splice(1, 0, {
        id: "collaborateurs",
        name: "Collaborateurs",
        href: `/structures/${structure.slug}/collaborateurs`,
      });
    }
  }

  $: {
    if ($page.url.pathname.endsWith("/services")) {
      tabId = "services";
    } else if ($page.url.pathname.endsWith("/modeles")) {
      tabId = "modeles";
    } else if ($page.url.pathname.endsWith("/antennes")) {
      tabId = "antennes";
    } else if ($page.url.pathname.endsWith("/collaborateurs")) {
      tabId = "collaborateurs";
    } else {
      tabId = "informations";
    }
  }
</script>

<h1 class="pt-s40 text-white">
  {capitalize(structure.name)}
</h1>

<Label
  label={`${structure.address1}${
    structure.address2 ? `, ${structure.address2}` : ""
  }, ${structure.postalCode} ${structure.city}`}
  icon={mapPinIcon}
  darkBg
  smallIcon
/>

{#if structure.isPendingMember}
  <div class="mt-s24"><PendingNotice /></div>
{:else if !structure.hasAdmin}
  <div class="mt-s24"><AdminNotice {structure} /></div>
{/if}

<div class="noprint mt-s24">
  <Tabs items={tabs} itemId={tabId} />
</div>

<style lang="postcss">
  @media print {
    h1 {
      color: var(--col-magenta-brand);
    }
  }
</style>
