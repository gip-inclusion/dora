<script>
  export let class1, class2;
</script>

<div class="flex {class1}">
  <div class="grid mx-auto grid-cols-main gap-x-3 gap-y-3 {class2}">
    <slot />
  </div>
</div>
