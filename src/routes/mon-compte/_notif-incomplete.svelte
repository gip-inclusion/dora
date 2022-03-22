<script>
  import LinkButton from "$lib/components/link-button.svelte";
</script>

<div class="mb-s16 lg:mb-s0">
  <h4 class="mb-s8 text-error">Informations incomplètes</h4>
  <p class="text-f14">
    Complétez votre compte afin de pouvoir utiliser toutes les fonctionnalités
    de DORA.
  </p>
</div>

<div class="self-end">
  <LinkButton label="Modifier…" to="/mon-compte/editer" small secondary />
</div>
