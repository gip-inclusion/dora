<script>
  import { onDestroy } from "svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  import ContributionPic from "$lib/assets/illu_contribution.svg";
  import { addCircleIcon } from "$lib/icons";
  import EmailButton from "$lib/components/email-button.svelte";

  import { id, duration } from "./_store";

  // initialise les valeur en quittant le composant
  onDestroy(() => {
    $id = null;
    $duration = null;
  });
</script>

<svelte:head>
  <title>Merci de votre contribution | DORA</title>
  <meta
    name="description"
    content="Aidez-nous à identifier et référencer l’ensemble de l’offre de l’insertion"
  />
</svelte:head>
<CenteredGrid extraClass="bg-gradient-to-b from-magenta-10 to-magenta-10/0">
  <div class="lg:flex lg:gap-s32">
    <div class="lg:flex-1">
      <img
        class="hidden flex-none lg:block"
        src={ContributionPic}
        alt="Illustration en bichromie avec un homme et une femme, face à face chacun dans un cercle, en train de prendre des notes, séparéss par des traits horizontaux abstraits, et une main tenant un crayon au premier plan."
      />
    </div>
    <div class="lg:flex-1">
      <h1 class="text-france-blue">Merci pour votre contribution</h1>

      <p class="mt-s24">
        Votre suggestion a été proposée. Une fois validée par la structure, elle
        sera visible sur DORA.
      </p>

      <div class="mb-s24 flex flex-col items-start gap-s16">
        <LinkButton
          label="Proposer un nouveau service"
          to={"/contribuer/saisie"}
          icon={addCircleIcon}
          iconOnRight
        />

        <EmailButton />
      </div>

      {#if $id && $duration}
        <div class="rounded-md border border-gray-03 p-s24">
          <div class="h-s512">
            <iframe
              src={`https://tally.so/embed/n0Q749?alignLeft=1&hideTitle=1&transparentBackground=1&serviceSuggestionId=${$id}&duration=${$duration}`}
              width="100%"
              height="512"
              frameborder="0"
              marginheight="0"
              marginwidth="0"
              title="Évaluation saisie - Contribution"
            />
          </div>
        </div>
      {/if}
    </div>
  </div>
</CenteredGrid>
