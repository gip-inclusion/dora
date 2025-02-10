<script lang="ts">
  export let checked = false;
</script>

<div
  class="checkbox h-s24 w-s24 border-gray-03 flex shrink-0 justify-center rounded-sm border"
>
  <div
    class="checkbox-mark h-s12 w-s12 bg-magenta-cta self-center"
    class:invisible={!checked}
  />
</div>

<style lang="postcss">
  @reference "../../../app.css";

  /* Ce symbole de case à cocher peut être coché de deux façons différente :
   * - En mettant la prop checked à true ;
   * - En plaçant le composant directement à la suite d'un <input type="checkbox" />.
   *
   * La deuxième façon utilise la déclaration CSS globale ci-dessous pour afficher la coche
   * lorsque l'<input type="checkbox" /> qui précède ce composant est dans l'état « checked ».
   *
   * Il n'est pas nécessaire d'utiliser la prop checked avec la deuxième façon.
   */
  :global(input[type="checkbox"]:checked + .checkbox .checkbox-mark) {
    @apply visible;
  }
</style>
