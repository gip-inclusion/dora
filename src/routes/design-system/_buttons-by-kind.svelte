<script>
  import Buttons from "./_buttons-by-size.svelte";
  export let secondary, tertiary;
</script>

<div>
  <h3>Normaux</h3>
  <div class="flex flex-col items-start gap-3">
    <Buttons label="Bouton Simple" {secondary} {tertiary} />
  </div>
</div>
<div>
  <h3>Grands</h3>
  <div class="flex flex-col items-start gap-3">
    <Buttons label="Bouton Big" big {secondary} {tertiary} />
  </div>
</div>
<div>
  <h3>Petits</h3>
  <div class="flex flex-col items-start gap-3">
    <Buttons label="Bouton Petit" small {secondary} {tertiary} />
  </div>
</div>
