<script lang="ts">
  export let title: string;
</script>

<section class="gap-s24 text-gray-text flex flex-col">
  <h2 class="text-f23 text-france-blue mb-s0 leading-32 font-bold">
    {title}
  </h2>
  <slot />
</section>
