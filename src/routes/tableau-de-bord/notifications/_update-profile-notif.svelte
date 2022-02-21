<script>
  import LinkButton from "$lib/components/link-button.svelte";
</script>

<div class="mb-s16 lg:mb-s0">
  <h4 class="mb-s8 text-error">Votre profil n’est pas complet !</h4>
  <p class="text-f14">
    Afin de pouvoir utiliser toutes les fonctionnalités DORA, il est nécessaire
    de compléter votre profil (moins de 2 minutes).
  </p>
</div>
<div class="shrink-0 self-end py-s16">
  <LinkButton to="/tableau-de-bord/profil" label="Compléter mon profil" />
</div>
