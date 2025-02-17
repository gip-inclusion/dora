<script lang="ts" context="module">
  export type TabItem = {
    id: string;
    name: string;
    icon: string;
    href: string;
  };
</script>

<script lang="ts">
  import { page } from "$app/stores";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import Label from "$lib/components/display/label.svelte";
  import TabsLink from "./tabs-links.svelte";
  import {
    bookReadLineIcon,
    fileInfoLineIcon,
    homeSmile2Icon,
    mapPinIcon,
    pageLineIcon,
    teamLineIcon,
  } from "$lib/icons";
  import { capitalize } from "$lib/utils/misc";
  import AdminNotice from "./admin-notice.svelte";
  import PendingNotice from "./pending-notice.svelte";
  import type { Structure } from "$lib/types";

  export let structure: Structure;
  export let tabId = "informations";

  let tabs: TabItem[] = [];

  $: {
    tabs = [
      {
        id: "informations",
        name: "Informations",
        icon: fileInfoLineIcon,
        href: `/structures/${structure.slug}`,
      },
    ];

    if (structure.canViewMembers) {
      tabs.push({
        id: "collaborateurs",
        name: "Collaborateurs",
        icon: teamLineIcon,
        href: `/structures/${structure.slug}/collaborateurs`,
      });
    }
    tabs.push({
      id: "services",
      name: "Services",
      icon: pageLineIcon,
      href: `/structures/${structure.slug}/services`,
    });

    if (structure.canEditServices) {
      tabs.push({
        id: "modeles",
        name: "Modèles",
        icon: bookReadLineIcon,
        href: `/structures/${structure.slug}/modeles`,
      });
    }

    if (!structure.parent && structure.branches?.length) {
      tabs.push({
        id: "antennes",
        name: "Antennes",
        icon: homeSmile2Icon,
        href: `/structures/${structure.slug}/antennes`,
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

<div class="pt-s40 print:py-s40 relative mx-auto max-w-6xl">
  <Breadcrumb {structure} currentLocation="structure-{tabId}" />

  <h1 class="pt-s40 print:text-magenta-brand text-white">
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
    <div class="mt-s24">
      <PendingNotice shortAdminNames={structure.shortAdminNames} />
    </div>
  {:else if !structure.hasAdmin}
    <div class="mt-s24">
      <AdminNotice {structure} />
    </div>
  {/if}

  <div class="mt-s40 print:hidden">
    <TabsLink items={tabs} itemId={tabId} />
  </div>
</div>
