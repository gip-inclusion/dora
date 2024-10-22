<script lang="ts">
  import ButtonMenu from "$lib/components/display/button-menu.svelte";
  import { arrowDownSIcon } from "$lib/icons";
  import ModerationLabel from "./moderation-label.svelte";
  import ModerationMenu from "./moderation-menu.svelte";

  export let entity, onRefresh;
</script>

<div class="flex flex-row items-center gap-s4 font-bold">
  Modération :
  <div class="flex items-center rounded border border-gray-01">
    <div class="px-s12 py-s6">
      <ModerationLabel
        status={entity.moderationStatus}
        date={entity.moderationDate}
      />
    </div>
    <div class="text-gray-02">|</div>
    <ButtonMenu icon={arrowDownSIcon} let:onClose={onCloseParent} small>
      <div class="w-max">
        <ModerationMenu
          {entity}
          onRefresh={async () => {
            await onCloseParent();
            await onRefresh();
          }}
        />
      </div>
    </ButtonMenu>
  </div>
</div>
