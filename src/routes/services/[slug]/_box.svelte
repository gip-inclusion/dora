<script>
  import Label from "$lib/components/label.svelte";
  import { compassFillIcon } from "$lib/icons";

  export let title = "";
</script>

<style lang="postcss">
  .wrapper {
    overflow: hidden;
    border: 3px solid var(--box-color);
    margin: var(-s20) 0;
    border-radius: var(--s8);
  }

  .title {
    padding-top: var(--s24);
    padding-bottom: var(--s24);
    padding-left: var(--s40);
    background: var(--box-color);
    color: var(--col-white);
  }

  .title h3 {
    color: var(--col-white);
  }

  @media print {
    .title {
      background: var(--col-white);
      color: var(--box-color);
    }

    .title h3 {
      color: var(--col-gray-dark);
    }
  }
</style>

<div class="wrapper">
  <div class="title">
    <Label icon={compassFillIcon} iconOnLeft darkBg bigIcon>
      <h3>{title}</h3>
    </Label>
  </div>
  <div class="p-s8 lg:p-s32">
    <slot />
  </div>
</div>
