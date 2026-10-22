<script lang="ts" module>
  export type HomeTabId = "accompagnement" | "porteurs" | "particuliers";

  export const homeTabs: { id: HomeTabId; name: string }[] = [
    { id: "accompagnement", name: "Professionnels de l’accompagnement" },
    { id: "porteurs", name: "Porteurs de services" },
    { id: "particuliers", name: "Particuliers" },
  ];
</script>

<script lang="ts">
  import illuAccompagner from "#lib/assets/illustrations/illu-accompagner.svg";
  import illuMobiliser from "#lib/assets/illustrations/illu-mobiliser.svg";
  import illuRecenser from "#lib/assets/illustrations/illu-recenser.svg";
  import ExternalLinkIcon from "#lib/components/display/external-link-icon.svelte";
  import {
    INCLUSION_PLATFORM_ORIENTATIONS_URL,
    INCLUSION_PLATFORM_SEARCH_URL,
  } from "#lib/consts.js";

  interface Props {
    tabId: HomeTabId;
  }

  let { tabId }: Props = $props();
</script>

<div
  class="gap-s24 flex flex-col md:flex-row md:justify-center"
  role="tabpanel"
  aria-labelledby={`tab-${tabId}`}
>
  {#if tabId === "accompagnement"}
    <div class="md:basis-1/3">
      <img src={illuRecenser} alt="" class="mb-s16 w-full" />
      <h3 class="text-france-blue">Identifiez des services</h3>
      <p class="text-f16">
        DORA vous permet d’<strong
          >identifier les services d’insertion les plus adaptés</strong
        >
        aux besoins spécifiques de vos bénéficiaires.
      </p>
    </div>
    <div class="md:basis-1/3">
      <img src={illuAccompagner} alt="" class="mb-s16 w-full" />
      <h3 class="text-france-blue">Orientez vos bénéficiaires</h3>
      <p class="text-f16">
        Le formulaire <strong
          >facilite l’orientation de vos bénéficiaires</strong
        >
        vers la solution identifiée. Il est maintenant intégré directement à la Plateforme
        de l’inclusion.
      </p>
      <a
        href={INCLUSION_PLATFORM_SEARCH_URL}
        target="_blank"
        rel="noopener"
        class="text-f14 text-magenta-cta font-bold"
      >
        Orientez votre bénéficiaire<ExternalLinkIcon />
      </a>
    </div>
    <div class="md:basis-1/3">
      <img src={illuMobiliser} alt="" class="mb-s16 w-full" />
      <h3 class="text-france-blue">Suivez vos demandes</h3>
      <p class="text-f16">
        <strong>Gardez une trace écrite de vos demandes</strong> et visualisez la
        réponse de la structure partenaire. Le tableau de suivi est maintenant intégré
        directement à la Plateforme de l’inclusion.
      </p>
      <a
        href={INCLUSION_PLATFORM_ORIENTATIONS_URL}
        target="_blank"
        rel="noopener"
        class="text-f14 text-magenta-cta font-bold"
      >
        Suivez vos demandes envoyées<ExternalLinkIcon />
      </a>
    </div>
  {:else if tabId === "porteurs"}
    <div class="md:basis-1/3">
      <img src={illuMobiliser} alt="" class="mb-s16 w-full" />
      <h3 class="text-france-blue">Suivez vos demandes reçues</h3>
      <p class="text-f16">
        <strong>Gardez une trace écrite de vos demandes reçues.</strong>
        Téléchargez la liste des orientations reçues par votre structure. Vous pourrez
        ainsi consulter et trier ces orientations. Fichier proposé au format .xls.
      </p>
    </div>
    <div class="md:basis-1/3">
      <img src={illuRecenser} alt="" class="mb-s16 w-full" />
      <h3 class="text-france-blue">
        Donnez de la visibilité à votre offre de services
      </h3>
      <p class="text-f16">
        Avec plus de <strong>68 000 visiteurs</strong> uniques par mois et
        <strong>180 000 services actifs</strong>, DORA est l’annuaire de
        l’insertion de référence.
      </p>
    </div>
    <div class="md:basis-1/3">
      <img src={illuAccompagner} alt="" class="mb-s16 w-full" />
      <h3 class="text-france-blue">Centralisez les mises à jour de services</h3>
      <p class="text-f16">
        Saisissez ou importez vos services et mettez-les à jour, en un seul
        endroit ! DORA se charge de présenter vos données là où elles sont
        utiles, en <strong
          >les diffusant automatiquement sur plusieurs sites.</strong
        >
      </p>
    </div>
  {:else if tabId === "particuliers"}
    <div class="md:basis-1/3">
      <img src={illuRecenser} alt="" class="mb-s16 w-full" />
      <h3 class="text-france-blue">Trouvez des services adaptés</h3>
      <p class="text-f16">
        DORA vous permet d’<strong
          >identifier les services d’insertion les plus adaptés</strong
        >
        à vos besoins.
      </p>
    </div>
    <div class="md:basis-1/3">
      <img src={illuAccompagner} alt="" class="mb-s16 w-full" />
      <h3 class="text-france-blue">Contactez les structures</h3>
      <p class="text-f16">
        Prenez contact avec les structures selon leurs préférences : téléphone,
        email, présentation à l’accueil, site du service…
      </p>
    </div>
  {/if}
</div>
