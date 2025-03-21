<script lang="ts">
  export let title: string;
</script>

<section>
  <h3 class="text-f17 leading-s24 text-gray-dark mb-s8 font-bold">
    {title}
  </h3>
  <slot />
</section>
