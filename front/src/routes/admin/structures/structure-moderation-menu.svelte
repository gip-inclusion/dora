<script lang="ts">
  import ArrowDownSLineArrows from "svelte-remix/ArrowDownSLineArrows.svelte";

  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import Button from "$lib/components/display/button.svelte";
  import Label from "$lib/components/display/label.svelte";
  import { setModerationState } from "$lib/requests/admin";
  import { modifyStructure } from "$lib/requests/structures";
  import type { AdminStructure, ModerationStatus } from "$lib/types";

  interface Props {
    structure: AdminStructure;
    onRefresh: () => Promise<void>;
  }

  let { structure, onRefresh }: Props = $props();

  const isValidated = $derived(structure.moderationStatus === "VALIDATED");

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
    {:else if isValidated}
      <Label label="Administrateurs validés" bold success />
    {:else}
      <Label label="Administrateurs à inviter ou valider" bold error />
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
          {#if isValidated}
            <Button
              label="Administrateurs à remodérer"
              onclick={async () => {
                onClose();
                await handleModeration("NEED_NEW_MODERATION");
              }}
              small
              noBackground
            />
          {:else}
            <Button
              label="Valider les administrateurs"
              onclick={async () => {
                onClose();
                await handleModeration("VALIDATED");
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
