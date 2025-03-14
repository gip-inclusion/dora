<script lang="ts">
  export let ariaLabel: string;
</script>

<button
  class="border-gray-03 text-gray-text-alt py-s12 px-s20 hover:text-magenta-cta hover:border-magenta-cta rounded-sm border-1"
  aria-label={ariaLabel}
  on:click
>
  <slot />
</button>
