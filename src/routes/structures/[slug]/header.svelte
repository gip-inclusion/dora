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
  import { userInfo } from "$lib/utils/auth";
  import { capitalize } from "$lib/utils/misc";
  import AdminNotice from "./admin-notice.svelte";
  import PendingNotice from "./pending-notice.svelte";

  export let structure;
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

    if (!structure.parent && structure.branches?.length) {
      tabs.splice(1, 0, {
        id: "antennes",
        name: "Antennes",
        icon: homeSmile2Icon,
        href: `/structures/${structure.slug}/antennes`,
      });
    }

    if (
      structure.models?.length &&
      (structure.isMember || $userInfo?.isStaff)
    ) {
      tabs.splice(1, 0, {
        id: "modeles",
        name: "Modèles",
        icon: bookReadLineIcon,
        href: `/structures/${structure.slug}/modeles`,
      });
    }

    if (structure.services?.length || structure.archivedServices?.length) {
      tabs.splice(1, 0, {
        id: "services",
        name: "Services",
        icon: pageLineIcon,
        href: `/structures/${structure.slug}/services`,
      });
    }
    if (structure.isMember || $userInfo?.isStaff || $userInfo?.isBizdev) {
      tabs.splice(1, 0, {
        id: "collaborateurs",
        name: "Collaborateurs",
        icon: teamLineIcon,
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

<div class="relative mx-auto max-w-6xl pt-s40">
  <Breadcrumb {structure} currentLocation="structure-{tabId}" />

  <h1 class="pt-s40 text-white print:text-magenta-brand">
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
      <PendingNotice />
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
