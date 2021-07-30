<script>
  import { coperCoinFillIcon } from "$lib/icons.js";
  import Button from "$lib/components/button.svelte";
</script>

<h1>Boutons</h1>
<div class="flex flex-row items-start gap-3">
  <div>
    <h2>Normaux</h2>
    <div class="flex flex-col items-start gap-3">
      <Button type="button" label="Bouton Simple" />
      <Button
        type="button"
        label="Bouton Simple"
        icon={coperCoinFillIcon}
        iconOnLeft />
      <Button
        type="button"
        label="Bouton Simple"
        icon={coperCoinFillIcon}
        iconOnRight />
      <Button type="button" icon={coperCoinFillIcon} />
      <Button
        type="button"
        label="Bouton Simple"
        disabled
        icon={coperCoinFillIcon}
        iconOnLeft />
    </div>
  </div>
  <div>
    <h2>Grands</h2>
    <div class="flex flex-col items-start gap-3">
      <Button type="button" label="Bouton Big" big />
      <Button
        type="button"
        label="Bouton Big"
        icon={coperCoinFillIcon}
        iconOnLeft
        big />
      <Button
        type="button"
        label="Bouton Big"
        icon={coperCoinFillIcon}
        iconOnRight
        big />
      <Button type="button" icon={coperCoinFillIcon} big />
      <Button
        type="button"
        label="Bouton Big"
        disabled
        icon={coperCoinFillIcon}
        iconOnLeft
        big />
    </div>
  </div>
  <div>
    <h2>Petits</h2>
    <div class="flex flex-col items-start gap-3">
      <Button type="button" label="Bouton Petit" small />
      <Button
        type="button"
        label="Bouton Petit"
        icon={coperCoinFillIcon}
        iconOnLeft
        small />
      <Button
        type="button"
        label="Bouton Petit"
        icon={coperCoinFillIcon}
        iconOnRight
        small />
      <Button type="button" icon={coperCoinFillIcon} small />
      <Button
        type="button"
        label="Bouton Petit"
        disabled
        icon={coperCoinFillIcon}
        iconOnLeft
        small />
    </div>
  </div>
</div>
