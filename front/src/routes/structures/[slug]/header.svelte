<script lang="ts" module>
  export type TabItem = {
    id: string;
    name: string;
    icon: string;
    href: string;
  };
</script>

<script lang="ts">
  import { run } from 'svelte/legacy';

  import HomeSmileLineBuildings from "svelte-remix/HomeSmileLineBuildings.svelte";
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

  interface Props {
    structure: Structure;
    tabId?: string;
  }

  let { structure, tabId = $bindable("informations") }: Props = $props();

  let tabs: TabItem[] = $state([]);

  run(() => {
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
  });

  run(() => {
    if ($page.url.pathname.includes("/services")) {
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
  });
</script>

<div class="text-gray-text pt-s32">
  <Breadcrumb {structure} currentLocation="structure-{tabId}" />

  <div class="mt-s48 gap-s12 flex flex-col">
    {#if structure.parent}
      <div class="gap-s6 text-f14 flex items-center">
        <HomeSmileLineBuildings size="16" />
        <strong>
          Structure parente&#8239;:
          <a href="/structures/{structure.parentSlug}" class="underline"
            >{capitalize(structure.parentName)}</a
          >
        </strong>
      </div>
    {/if}

    <h1 class="text-magenta-dark text-f38 leading-s48 m-s0">
      {capitalize(structure.name)}
    </h1>

    <Label
      label={`${structure.address1}${
        structure.address2 ? `, ${structure.address2}` : ""
      }, ${structure.postalCode} ${structure.city}`}
      icon={mapPinIcon}
      smallIcon
    />
  </div>

  {#if structure.isPendingMember}
    <div class="mt-s24">
      <PendingNotice shortAdminNames={structure.shortAdminNames} />
    </div>
  {:else if !structure.hasAdmin}
    <div class="mt-s24">
      <AdminNotice {structure} />
    </div>
  {/if}

  <div class="mt-s20 print:hidden">
    <TabsLink items={tabs} itemId={tabId} />
  </div>
</div>
