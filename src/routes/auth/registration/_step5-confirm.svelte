<script>
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Info from "$lib/components/info.svelte";
  import { registrationInfo } from "./_store.js";
</script>

<Fieldset
  title="Confirmation"
  description="Chaque utilisateur DORA est attaché à une structure d’insertion (de l’Etat ou associative/independante. Afin de mieux vous aider à identifier votre structure, merci de choisir la typologie de votre structure :"
>
  <Info label="Votre demande a été enregistrée" positiveMood>
    <p class="mb-s16">
      Un e-mail vous a été envoyé à l’adresse <strong
        >{$registrationInfo.email}</strong
      >. Cliquez sur le lien reçu afin de valider la création de votre compte.
    </p>
    <p>
      Si d’ici 10 minutes vous n’avez toujours rien reçu, consultez votre
      dossier « indésirable » ou « spam ». Si le problème persiste,
      <a
        class="underline"
        target="_blank"
        rel="noopener nofollow"
        href="https://itou.typeform.com/doracontactsupp">contactez-nous</a
      >.
    </p>
  </Info>
</Fieldset>
