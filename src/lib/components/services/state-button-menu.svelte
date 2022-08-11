<script>
  import { arrowDownSIcon } from "$lib/icons";

  import ButtonMenu from "$lib/components/button-menu.svelte";
  import StateMenu from "./state-menu.svelte";
  import StateLabel from "./state-label.svelte";

  export let service, servicesOptions;
  export let onRefresh;
</script>

<div class="flex items-center rounded border border-gray-01">
  <div class="px-s12 py-s6"><StateLabel {service} /></div>
  <div class="text-gray-02">|</div>

  <ButtonMenu icon={arrowDownSIcon} let:onClose={onCloseParent} small>
    <StateMenu
      {service}
      {servicesOptions}
      onRefresh={async () => {
        await onCloseParent();
        await onRefresh();
      }}
    />
  </ButtonMenu>
</div>
