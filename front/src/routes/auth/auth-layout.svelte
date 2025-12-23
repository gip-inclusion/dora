<script lang="ts">
  import type { Snippet } from "svelte";

  import connexionPic from "$lib/assets/illustrations/illu-connexion.svg";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";

  interface Props {
    children?: Snippet;
  }

  let { children }: Props = $props();
</script>

<CenteredGrid bgColor="bg-magenta-10">
  <div class="gap-s24 flex flex-col lg:flex-row">
    <div class="mt-s48 hidden justify-center lg:flex lg:w-1/2">
      <img src={connexionPic} alt="" class="max-h-[460px]" />
    </div>
    <div class="lg:w-1/2">
      {@render children?.()}
    </div>
  </div>
</CenteredGrid>
