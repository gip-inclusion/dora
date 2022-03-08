<script>
  import { mailIcon } from "$lib/icons";
  import LinkButton from "./link-button.svelte";
  export let wFull = false;

  const sharingEmailSubject = encodeURIComponent("Connaissez-vous Dora ?");
  const sharingEmailBody = encodeURIComponent(
    `
Bonjour,
Je me permets de vous partager un projet qui devrait vous intéresser.

Connaissez-vous Dora ?

Lancé en Mai 2021, Dora est un service public numérique porté par la DGEFP qui permet aux structures de l'insertion de référencer simplement et mettre à jour en temps réel leur offre de services, et aux professionnels prescripteurs de rechercher et mobiliser rapidement le service le plus adapté au besoin de leur bénéficiaire.

J'ai le plaisir de vous annoncer que Dora est accessible dès aujourd'hui pour l'ensemble les acteurs de l'insertion du territoire. De nombreux partenaires ont d'ores et déjà mis en visibilité leur offre de service sur Dora. Vous pouvez également vous inscrire et bénéficier de ce service !

👉 Pour accéder à Dora cliquez sur ce lien (pensez à l'ajouter à vos favoris 😉) :
https://dora.fabrique.social.gouv.fr/

Dans l'attente de pouvoir consulter votre offre de service sur cet outil.
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
