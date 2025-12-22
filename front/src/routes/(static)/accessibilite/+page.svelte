<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import { URL_HELP_SITE } from "$lib/consts";
</script>

<CenteredGrid>
  <div class="max-w-3xl">
    <div class="mb-s48">
      <Breadcrumb currentLocation="accessibility" />
    </div>

    <h1>Déclaration d’accessibilité</h1>
    <p>Établie le <span>7 décembre 2022</span>.</p>
    <p>
      <span>Le GIP Plateforme de l’inclusion</span> s’engage à rendre son service
      accessible, conformément à l’article 47 de la loi n° 2005-102 du 11 février
      2005.
    </p>
    <p>
      Cette déclaration d’accessibilité s’applique à <strong>DORA</strong>
      <span> (https://dora.inclusion.beta.gouv.fr/)</span>.
    </p>
    <h2>État de conformité</h2>
    <p>
      <strong>DORA</strong> est
      <strong><span data-printfilter="lowercase">non conforme</span></strong>
      avec le
      <abbr title="Référentiel général d’amélioration de l’accessibilité"
        >RGAA</abbr
      >. <span>Le site n’a encore pas été audité.</span>
    </p>
    <h2>Établissement de cette déclaration d’accessibilité</h2>
    <p>Cette déclaration a été établie le <span>7 décembre 2022</span>.</p>
    <h3>Technologies utilisées</h3>
    <p>
      L’accessibilité de <span>DORA</span> s’appuie sur les technologies suivantes&nbsp;:
    </p>
    <ul class="technical-information technologies-used">
      <li>HTML</li>
      <li>WAI-ARIA</li>
      <li>CSS</li>
      <li>JavaScript</li>
    </ul>
    <h2>Amélioration et contact</h2>
    <p>
      Si vous n’arrivez pas à accéder à un contenu ou à un service, vous pouvez
      contacter le responsable de <span>DORA</span> pour être orienté vers une alternative
      accessible ou obtenir le contenu sous une autre forme.
    </p>
    <ul class="basic-information feedback h-card">
      <li>
        E-mail&nbsp;: <a href="mailto:support.dora@inclusion.gouv.fr"
          >support.dora@inclusion.gouv.fr</a
        >
      </li>

      <li>
        Formulaire de contact&nbsp;: <a href={URL_HELP_SITE}>{URL_HELP_SITE}</a>
      </li>
      <li>
        Adresse&nbsp;: <span>127 rue de Grenelle 75007 Paris </span>
      </li>
    </ul>
    <h2>Voie de recours</h2>
    <p>
      Cette procédure est à utiliser dans le cas suivant&nbsp;: vous avez
      signalé au responsable du site internet un défaut d’accessibilité qui vous
      empêche d’accéder à un contenu ou à un des services du portail et vous
      n’avez pas obtenu de réponse satisfaisante.
    </p>
    <p>Vous pouvez&nbsp;:</p>
    <ul>
      <li>
        Écrire un message au <a href="https://formulaire.defenseurdesdroits.fr/"
          >Défenseur des droits</a
        >
      </li>
      <li>
        Contacter <a href="https://www.defenseurdesdroits.fr/saisir/delegues"
          >le délégué du Défenseur des droits dans votre région</a
        >
      </li>
      <li>
        Envoyer un courrier par la poste (gratuit, ne pas mettre de
        timbre)&nbsp;:<br />
        Défenseur des droits<br />
        Libre réponse 71120 75342 Paris CEDEX 07
      </li>
    </ul>
    <hr />
    <p>
      Cette déclaration d’accessibilité a été créé le <span
        >7 décembre 2022</span
      >
      grâce au
      <a href="https://betagouv.github.io/a11y-generateur-declaration/#create"
        >Générateur de Déclaration d’Accessibilité de BetaGouv</a
      >.
    </p>
  </div>
</CenteredGrid>

<style lang="postcss">
  @reference "../../../app.css";

  h1 {
    @apply text-france-blue;
  }

  a {
    @apply underline;
  }

  h2 {
    @apply mb-s24 mt-s48;
  }

  li {
    @apply list-inside list-disc;
  }

  hr {
    @apply my-s32;
  }
</style>
