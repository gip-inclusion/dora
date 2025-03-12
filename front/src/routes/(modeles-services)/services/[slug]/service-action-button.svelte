<script lang="ts">
  export let ariaLabel: string;
</script>

<button
  class="border-gray-03 text-gray-text-alt py-s12 px-s20 hover:text-magenta-cta hover:border-magenta-cta border-1"
  {ariaLabel}
  on:click
>
  <slot />
</button>
