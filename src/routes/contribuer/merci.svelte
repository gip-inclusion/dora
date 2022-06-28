<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  import ContributionPic from "$lib/assets/illu_contribution.svg";
  import { addCircleIcon } from "$lib/icons";
  import EmailButton from "$lib/components/email-button.svelte";
</script>

<svelte:head>
  <title>Merci de votre contribution | DORA</title>
  <meta
    name="description"
    content="Aidez-nous à identifier et référencer l’ensemble de l’offre de l’insertion"
  />
</svelte:head>
<CenteredGrid extraClass="bg-gradient-to-b from-magenta-10 to-magenta-10/0">
  <div class="flex gap-s24">
    <img
      class="flex-none"
      src={ContributionPic}
      width="587"
      height="532"
      alt=""
    />
    <div class="flex-1">
      <h1 class="text-france-blue">Merci pour votre contribution</h1>

      <p class="mt-s24">
        Votre suggestion a été proposée. Une fois validée par la structure, elle
        sera visible sur DORA.
      </p>

      <div class="flex flex-col items-start gap-s16">
        <LinkButton
          label="Proposer un nouveau service"
          to={"/contribuer/saisie"}
          icon={addCircleIcon}
          iconOnRight
        />

        <EmailButton />
      </div>
    </div>
  </div>
</CenteredGrid>
