<script>
  import { arrowDownSIcon } from "$lib/icons";

  import ButtonMenu from "$lib/components/button-menu.svelte";
  import ModerationMenu from "./_moderation-menu.svelte";
  import ModerationLabel from "./_moderation-label.svelte";

  export let entity, onRefresh;
</script>

<div class="flex flex-row items-center gap-s4 font-bold">
  Modération :
  <div class="flex items-center rounded border border-gray-01">
    <div class="px-s12 py-s6">
      <ModerationLabel
        status={entity.moderationStatus}
        date={entity.moderationDate}
      />
    </div>
    <div class="text-gray-02">|</div>
    <ButtonMenu icon={arrowDownSIcon} let:onClose={onCloseParent} small>
      <ModerationMenu
        {entity}
        onRefresh={async () => {
          await onCloseParent();
          await onRefresh();
        }}
      />
    </ButtonMenu>
  </div>
</div>
