<script>
  import ButtonsKinds from "./_buttons-by-kind.svelte";
</script>

<h1>Boutons</h1>
<h2>Principaux</h2>
<div class="flex flex-row items-start gap-3">
  <ButtonsKinds />
</div>
<h2>Secondaires</h2>
<div class="flex flex-row items-start gap-3">
  <ButtonsKinds secondary />
</div>
<h2>Tertiaires</h2>
<div class="flex flex-row items-start gap-3">
  <ButtonsKinds tertiary />
</div>
