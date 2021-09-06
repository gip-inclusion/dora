<script>
  import Label from "$lib/components/label.svelte";
  import { compassFillIcon } from "$lib/icons";

  export let title = "";
</script>

<style>
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

  .content {
    padding: var(--s32) var(--s40) var(--s40);
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
  <div class="content">
    <slot />
  </div>
</div>
