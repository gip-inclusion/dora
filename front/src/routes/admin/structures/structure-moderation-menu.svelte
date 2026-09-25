<script lang="ts">
  import ArrowDownSLineArrows from "svelte-remix/ArrowDownSLineArrows.svelte";

  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import Button from "$lib/components/display/button.svelte";
  import Label from "$lib/components/display/label.svelte";
  import { setModerationState } from "$lib/requests/admin";
  import { modifyStructure } from "$lib/requests/structures";
  import type { AdminStructure, ModerationStatus } from "$lib/types";

  import { getAdminsBadge } from "./structure-statuses";

  interface Props {
    structure: AdminStructure;
    onRefresh: () => Promise<void>;
  }

  let { structure, onRefresh }: Props = $props();

  // Le statut de modération (`structure.moderationStatus`) ne décrivait pas à
  // lui seul la situation des administrateurs : il restait généralement à
  // `VALIDATED` même sur une structure à laquelle plus aucun administrateur
  // n'était rattaché. On réutilise donc le statut affiché sur la carte, qui
  // tient compte des membres de la structure.
  const adminsBadge = $derived(getAdminsBadge(structure));
  // La modération porte sur les administrateurs déjà rattachés à la structure :
  // elle n'a pas de sens lorsqu'il n'y en a aucun.
  const canValidateAdmins = $derived(structure.adminsToModerate.length > 0);

  async function handleModeration(status: ModerationStatus) {
    await setModerationState(structure, status);
    await onRefresh();
  }

  async function handleObsolete(isObsolete: boolean) {
    await modifyStructure({ slug: structure.slug, isObsolete });
    await onRefresh();
  }
</script>

<div class="border-gray-01 inline-flex items-center rounded-sm border">
  <div class="px-s12 py-s6">
    {#if structure.isObsolete}
      <Label label="Structure désactivée" bold error />
    {:else}
      <Label
        label={adminsBadge.label}
        bold
        success={adminsBadge.color === "green"}
        wait={adminsBadge.color === "orange"}
        error={adminsBadge.color === "red"}
      />
    {/if}
  </div>
  <div class="text-gray-02">|</div>
  <ButtonMenu
    icon={ArrowDownSLineArrows}
    small
    hideLabel
    label="Actions de modération"
  >
    {#snippet children({ onClose })}
      <div class="flex w-max flex-col items-end">
        {#if structure.isObsolete}
          <Button
            label="Réactiver la structure"
            onclick={async () => {
              onClose();
              await handleObsolete(false);
            }}
            small
            noBackground
            extraClass="text-success!"
          />
        {:else}
          {#if canValidateAdmins}
            <Button
              label="Valider les administrateurs"
              onclick={async () => {
                onClose();
                await handleModeration("VALIDATED");
              }}
              small
              noBackground
            />
          {:else if structure.hasAdmin}
            <Button
              label="Administrateurs à remodérer"
              onclick={async () => {
                onClose();
                await handleModeration("NEED_NEW_MODERATION");
              }}
              small
              noBackground
            />
          {/if}
          <Button
            label="Désactiver la structure"
            onclick={async () => {
              onClose();
              await handleObsolete(true);
            }}
            small
            noBackground
            extraClass="text-error!"
          />
        {/if}
      </div>
    {/snippet}
  </ButtonMenu>
</div>
