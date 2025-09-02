<script lang="ts" module>
  import type { Component } from "svelte";

  export type TabItem = {
    id: string;
    name: string;
    icon: Component;
    href: string;
  };
</script>

<script lang="ts">
  import BookReadLineDocument from "svelte-remix/BookReadLineDocument.svelte";
  import FileInfoLineDocument from "svelte-remix/FileInfoLineDocument.svelte";
  import HomeSmileLineBuildings from "svelte-remix/HomeSmileLineBuildings.svelte";
  import HomeSmile2LineBuildings from "svelte-remix/HomeSmile2LineBuildings.svelte";
  import MapPin2LineMap from "svelte-remix/MapPin2LineMap.svelte";
  import PagesLineDocument from "svelte-remix/PagesLineDocument.svelte";
  import TeamLineUserFaces from "svelte-remix/TeamLineUserFaces.svelte";

  import { page } from "$app/stores";

  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import Label from "$lib/components/display/label.svelte";
  import type { Structure } from "$lib/types";
  import { capitalize } from "$lib/utils/misc";

  import TabsLink from "./tabs-links.svelte";

  import AdminNotice from "./admin-notice.svelte";
  import PendingNotice from "./pending-notice.svelte";

  interface Props {
    structure: Structure;
  }

  let { structure }: Props = $props();

  let tabs: TabItem[] = $derived.by(() => {
    const tabList = [
      {
        id: "informations",
        name: "Informations",
        icon: FileInfoLineDocument,
        href: `/structures/${structure.slug}`,
      },
    ];

    if (structure.canViewMembers) {
      tabList.push({
        id: "collaborateurs",
        name: "Collaborateurs",
        icon: TeamLineUserFaces,
        href: `/structures/${structure.slug}/collaborateurs`,
      });
    }
    tabList.push({
      id: "services",
      name: "Services",
      icon: PagesLineDocument,
      href: `/structures/${structure.slug}/services`,
    });

    if (structure.canEditServices) {
      tabList.push({
        id: "modeles",
        name: "Modèles",
        icon: BookReadLineDocument,
        href: `/structures/${structure.slug}/modeles`,
      });
    }

    if (!structure.parent && structure.branches?.length) {
      tabList.push({
        id: "antennes",
        name: "Antennes",
        icon: HomeSmile2LineBuildings,
        href: `/structures/${structure.slug}/antennes`,
      });
    }

    return tabList;
  });

  let tabId = $derived.by(() => {
    if ($page.url.pathname.includes("/services")) {
      return "services";
    } else if ($page.url.pathname.endsWith("/modeles")) {
      return "modeles";
    } else if ($page.url.pathname.endsWith("/antennes")) {
      return "antennes";
    } else if ($page.url.pathname.endsWith("/collaborateurs")) {
      return "collaborateurs";
    } else {
      return "informations";
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
      icon={MapPin2LineMap}
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
