<script>
  export let title;
</script>

<div
  class="flex flex-col max-w-4xl gap-6 pt-4 mt-6 bg-white rounded-md shadow-sm px-7 pb-7 ">
  <h3>
    {title}
  </h3>

  <slot />
</div>
