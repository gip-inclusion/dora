<script>
  import { mailIcon } from "$lib/icons";
  import LinkButton from "./link-button.svelte";
  export let wFull = false;

  const sharingEmailSubject = encodeURIComponent("Connaissez-vous Dora ?");
  const sharingEmailBody = encodeURIComponent(
    `
Bonjour,

Je me permets de vous partager un service qui devrait vous intéresser.

Connaissez-vous Dora ?

Lancé en Mai 2021, Dora est un service public numérique porté par la DGEFP pour recenser l'offre d'insertion.
- Les structures de l'insertion référencent simplement et mettent à jour leur offre de services.
- Les professionnels prescripteurs recherchent et mobilisent rapidement le service adapté aux besoins de leurs bénéficiaires.

De nombreux partenaires ont déjà publié leur offre de service sur Dora. Vous pouvez également vous y inscrire.

👉 Cliquez sur ce lien (et pensez à l'ajouter à vos favoris) :
https://dora.fabrique.social.gouv.fr/

Dans l'attente de consulter votre offre de services.

Cordialement,
`.trim()
  );
</script>

<LinkButton
  label="Inviter un porteur de service"
  icon={mailIcon}
  iconOnRight
  secondary
  {wFull}
  to="mailto:?subject={sharingEmailSubject}&body={sharingEmailBody}"
/>
