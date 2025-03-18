<script lang="ts">
  import type { ComponentType } from "svelte";

  export let icon: ComponentType;
  export let title: string;
</script>

<section>
  <div class="gap-s8 flex">
    <div class="text-france-blue flex-shrink-0">
      <svelte:component this={icon} />
    </div>
    <div class="flex-grow">
      <h3 class="text-f17 text-france-blue mb-s8 leading-24">
        {title}
      </h3>
      <slot />
    </div>
  </div>
</section>
