<script lang="ts">
  import { mailIcon } from "$lib/icons";
  import LinkButton from "../display/link-button.svelte";

  export let wFull = false;

  const sharingEmailSubject = encodeURIComponent(
    "Référencement de votre offre d'insertion"
  );
  const sharingEmailBody = encodeURIComponent(
    `
Bonjour,

J’ai identifié votre structure car les services qu’elle propose me semblent tout à fait adaptés au dispositif DORA.

DORA est une initiative portée par la Ministre du Travail, de l’Emploi et de l’Insertion et mise en œuvre dans le cadre de la création du SPIE (Service Public de l’Insertion et de l’Emploi). Il s‘agit de l‘outil de référencement national de l‘offre d‘insertion sociale, socioprofessionnelle et professionnelle.

DORA va référencer gratuitement l‘ensemble des services de mobilités dédiés aux personnes exclues durablement de l‘emploi. Vous pourrez par la suite simplement mettre à jour en temps réel votre offre de services. Il permettra aux professionnels de l‘accompagnement social et professionnel de rechercher et mobiliser rapidement le service le plus adapté au besoin de leur bénéficiaire.

Pour en savoir plus, je vous suggère de vous inscrire au prochain webinaire de démo :
👩‍💻 Je m‘inscris ici : https://app.livestorm.co/dora-1


[DORA] Les documents et liens utiles :

🚀 Le lien d‘accès au site : https://dora.fabrique.social.gouv.fr/
🖥 Les tutoriels vidéos : https://www.youtube.com/channel/UCadIsy9gfHgLmLkutRGC5ew
📚 La documentation dora : https://aide.dora.fabrique.social.gouv.fr/fr/
👩‍💻 Lien d‘accès aux ateliers et webinaires d‘appropriation Dora : https://app.livestorm.co/dora-1

En espérant vous voir très bientôt sur Dora !
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
