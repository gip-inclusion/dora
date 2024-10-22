<script lang="ts">
  import ContributionPic from "$lib/assets/illustrations/illu-contribution.svg";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { addCircleIcon } from "$lib/icons";
</script>

<CenteredGrid extraClass="bg-gradient-to-b from-magenta-10 to-magenta-10/0">
  <div class="lg:flex lg:gap-s32">
    <div class="lg:flex-1">
      <img class="hidden flex-none lg:block" src={ContributionPic} alt="" />
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
      </div>

      <iframe
        src="https://tally.so/embed/n0Q749?alignLeft=1&hideTitle=1&transparentBackground=1"
        width="100%"
        height="512"
        frameborder="0"
        marginheight="0"
        marginwidth="0"
        title="Formulaire d’évaluation de la proposition d’un service"
      />
    </div>
  </div>
</CenteredGrid>
