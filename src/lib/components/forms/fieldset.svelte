<script>
  export let title;
</script>

<h2>
  {title}
</h2>
<div class="flex flex-col max-w-xl gap-6 p-8 mx-auto mt-8 bg-gray-bg">
  <slot />
</div>
