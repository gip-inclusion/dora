<script lang="ts">
  import ArrowDownSLineArrows from "svelte-remix/ArrowDownSLineArrows.svelte";
  import ArrowUpSLineArrows from "svelte-remix/ArrowUpSLineArrows.svelte";

  import LinkButton from "$lib/components/display/link-button.svelte";
  import Spinner from "$lib/components/display/spinner.svelte";
  import { getStructureAdmin } from "$lib/requests/admin";
  import type { AdminStructure, StructureMember } from "$lib/types";

  import EmailLine from "../email-line.svelte";
  import History from "../history.svelte";
  import UserInfo from "../user-info.svelte";
  import {
    getStructureStatusBadges,
    type StructureStatusColor,
  } from "./structure-statuses";
  import StructureEditLinks from "./structure-edit-links.svelte";
  import StructureModerationMenu from "./structure-moderation-menu.svelte";

  // Champs supplémentaires renvoyés lorsqu'on consulte le détail d'une structure.
  type AdminStructureDetails = AdminStructure & {
    members: StructureMember[];
    notes: { date: string; message: string; user?: { email: string } }[];
  };

  interface Props {
    structure: AdminStructure;
    highlighted: boolean;
    onHover: (slug: string | null) => void;
    onRefresh: () => void;
  }

  let { structure, highlighted, onHover, onRefresh }: Props = $props();

  const DOT_COLORS: Record<StructureStatusColor, string> = {
    green: "bg-success",
    orange: "bg-warning",
    red: "bg-error",
    gray: "bg-gray-text-alt",
  };

  let expanded = $state(false);
  // Les informations supplémentaires sont chargées lors du premier dépliage de la carte.
  let details = $state<AdminStructureDetails | null>(null);
  let loadingDetails = $state(false);

  const badges = $derived(getStructureStatusBadges(structure));
  const administrators = $derived(
    details?.members?.filter((member) => member.isAdmin) ?? []
  );
  const panelId = $derived(`structure-card-${structure.slug}`);

  async function loadDetails() {
    loadingDetails = true;
    try {
      details = (await getStructureAdmin(
        structure.slug
      )) as AdminStructureDetails;
    } finally {
      loadingDetails = false;
    }
  }

  function toggle() {
    expanded = !expanded;
    if (expanded && !details) {
      loadDetails();
    }
  }

  async function handleModerationRefresh() {
    await loadDetails();
    onRefresh();
  }
</script>

<div
  class="border-gray-01 rounded-lg border bg-white shadow-xs"
  class:highlight={highlighted}
  role="presentation"
  onmouseenter={() => onHover(structure.slug)}
  onmouseleave={() => onHover(null)}
>
  <button
    type="button"
    class="gap-s16 p-s24 flex w-full flex-row items-start justify-between text-left"
    aria-expanded={expanded}
    aria-controls={panelId}
    onclick={toggle}
  >
    <div class="gap-s4 flex flex-col">
      <h3 class="text-f20 text-france-blue mb-s0 leading-28">
        {structure.name}
      </h3>
      <p
        class="gap-x-s6 text-f14 text-gray-text mb-s0 flex flex-row flex-wrap items-center"
      >
        {#each badges as badge}
          <span class="gap-s4 inline-flex items-center">
            <span
              class="h-s10 w-s10 inline-block shrink-0 rounded-full {DOT_COLORS[
                badge.color
              ]}"
              aria-hidden="true"
            ></span>
            {badge.label}
          </span>
        {/each}
      </p>
    </div>
    <span class="text-magenta-cta shrink-0">
      {#if expanded}
        <ArrowUpSLineArrows size="24" />
      {:else}
        <ArrowDownSLineArrows size="24" />
      {/if}
    </span>
  </button>

  {#if expanded}
    <div
      id={panelId}
      class="border-gray-01 gap-s24 p-s24 flex flex-col border-t"
    >
      {#if loadingDetails && !details}
        <div class="flex justify-center">
          <Spinner />
        </div>
      {:else if details}
        <div class="gap-s16 flex flex-row flex-wrap justify-between">
          <section>
            <h4 class="mb-s8">Modération</h4>
            <StructureModerationMenu
              structure={details}
              onRefresh={handleModerationRefresh}
            />
          </section>

          <LinkButton
            label="Accéder à la fiche complète"
            to="/admin/structures/{structure.slug}"
            extraClass="self-start"
            otherTab
            secondary
            small
          />
        </div>

        {#if administrators.length}
          <section>
            <h4 class="mb-s8">Administrateurs•trices</h4>
            <ul class="gap-s8 pl-s20 flex list-disc flex-col">
              {#each administrators as administrator}
                <li>
                  <UserInfo user={administrator.user} structure={details} />
                </li>
              {/each}
            </ul>
          </section>
        {/if}

        {#if details.phone || details.email}
          <section>
            <h4 class="mb-s8">Informations de contact génériques</h4>
            {#if details.phone}<div>📞 {details.phone}</div>{/if}
            <EmailLine email={details.email} />
          </section>
        {/if}

        {#if details.notes?.length}
          <section class="text-f12">
            <h4 class="mb-s8">Historique</h4>
            <History notes={details.notes} />
          </section>
        {/if}

        <StructureEditLinks structureSlug={structure.slug} small />
      {/if}
    </div>
  {/if}
</div>

<style lang="postcss">
  @reference "../../../app.css";

  .highlight {
    @apply shadow-md;
  }

  h4 {
    @apply text-f16 text-gray-dark font-bold;
  }
</style>
