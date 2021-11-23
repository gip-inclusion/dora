<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import connexionPic from "$lib/assets/illu_connexion-optimise.svg";
  export let wideForm = false;
</script>

<CenteredGrid roundedbg>
  <div class="col-span-full flex justify-center lg:col-end-7 lg:mb-s32 mt-s48">
    <img src={connexionPic} alt="" class="max-h-[460px]" />
  </div>
  <div
    class="col-span-full lg:col-start-7 lg:col-end-12 mb-s32"
    class:lg:col-end-13={wideForm}
  >
    <slot />
  </div>
</CenteredGrid>
