<script lang="ts">
  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import { arrowDownSIcon } from "$lib/icons";
  import ModerationLabel from "./moderation-label.svelte";
  import ModerationMenu from "./moderation-menu.svelte";

  let { entity, onRefresh } = $props();
</script>

<div class="gap-s4 flex flex-row items-center font-bold">
  Modération :
  <div class="border-gray-01 flex items-center rounded-sm border">
    <div class="px-s12 py-s6">
      <ModerationLabel
        status={entity.moderationStatus}
        date={entity.moderationDate}
      />
    </div>
    <div class="text-gray-02">|</div>
    <ButtonMenu icon={arrowDownSIcon}  small>
      {#snippet children({ onClose: onCloseParent })}
            <div class="w-max">
          <ModerationMenu
            {entity}
            onRefresh={async () => {
              await onCloseParent();
              await onRefresh();
            }}
          />
        </div>
                {/snippet}
        </ButtonMenu>
  </div>
</div>
