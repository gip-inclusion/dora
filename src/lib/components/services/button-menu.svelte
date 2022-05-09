<script>
  import { moreIcon } from "$lib/icons";

  import ButtonMenu from "$lib/components/button-menu.svelte";
  import Menu from "./menu.svelte";

  export let service;
  export let onRefresh;
</script>

<ButtonMenu icon={moreIcon} let:onClose={onCloseParent}>
  <Menu
    {service}
    onRefresh={async () => {
      await onCloseParent();
      await onRefresh();
    }}
  />
</ButtonMenu>
