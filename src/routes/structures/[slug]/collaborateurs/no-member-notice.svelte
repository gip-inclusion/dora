<script lang="ts">
  import { teamLineIcon } from "$lib/icons";
  import illuMember from "$lib/assets/illustrations/collaborateurs.svg";
  import EmptyNotice from "../empty-notice.svelte";
</script>

<EmptyNotice
  textTopIcon={teamLineIcon}
  illustration={illuMember}
  title="Vous n’avez pas encore invité vos collaborateurs"
  links={[
    {
      url: "https://aide.dora.inclusion.beta.gouv.fr/fr/article/inviter-un-collaborateur-1e3lyy2/",
      label: "Découvrez comment gérer les collaborateurs",
    },
  ]}
>
  <div class="text-center leading-24">
    Invitez vos collègues à rejoindre votre structure sur DORA et partagez-vous
    les différentes tâches de gestion. En tant qu’administrateur de la
    structure, vous pouvez choisir le niveau de droits que vous accordez aux
    différents collègues, accepter les demandes d’adhésion ou bien révoquer
    l‘accès à un compte.
  </div>
</EmptyNotice>
