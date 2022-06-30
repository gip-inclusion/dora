<script>
  import { onDestroy, onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { serviceSlug, duration } from "$lib/components/services/form/_store";

  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Button from "$lib/components/button.svelte";

  function next() {
    if ($serviceSlug) {
      // replaceState évite que cette page soit dans l'historique
      goto(`/services/${$serviceSlug}`, { replaceState: true });
    } else {
      goto(`/`, { replaceState: true });
    }
  }

  onMount(() => {
    // si $id et $duration ne sont pas définis
    // l'utilisateur ne vient pas de valider le formulaire
    // -> quitte la page
    if ($serviceSlug && $duration) {
      return;
    }

    next();
  });

  // initialise les valeur en quittant le composant
  onDestroy(() => {
    $serviceSlug = null;
    $duration = null;
  });
</script>

<svelte:head>
  <title>Donnez votre avis | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1>Donnez votre avis</h1>
  </CenteredGrid>

  <hr />
  <CenteredGrid bgColor="bg-gray-bg">
    <div class="my-s24 rounded-md border border-gray-03 p-s24">
      <div class="h-s512">
        <iframe
          src={`https://tally.so/embed/n0Q749?alignLeft=1&hideTitle=1&transparentBackground=1&serviceSlug=${$serviceSlug}&duration=${$duration}`}
          width="100%"
          height="512"
          frameborder="0"
          marginheight="0"
          marginwidth="0"
          title="Évaluation saisie - Contribution"
        />
      </div>
    </div>
  </CenteredGrid>

  <hr />
  <CenteredGrid>
    <Button on:click={next} label="Continuer" />
  </CenteredGrid>
</EnsureLoggedIn>
