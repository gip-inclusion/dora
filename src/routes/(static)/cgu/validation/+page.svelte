<script lang="ts">
  import { goto } from "$app/navigation";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import StaticMarkdown from "$lib/components/display/static-markdown.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { refreshUserInfo } from "$lib/utils/auth";
  import { acceptCgu } from "$lib/utils/cgu";
  import type { PageData } from "./$types";

  export let data: PageData;
  let cguCanBeValidated = false;

  async function doAcceptCgu() {
    await acceptCgu();
    await refreshUserInfo();
    goto(data.next || "/");
  }
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <div class="mb-s48">
      <Breadcrumb currentLocation="cgu" dark />
    </div>

    <h1 class="mb-s32 text-france-blue">
      Mise à jour des Conditions Générales d’Utilisation de DORA
    </h1>

    <div
      class="cgu mb-s48 max-h-s512 overflow-auto rounded-md bg-blue-light p-s32"
      on:scroll={(evt) => {
        const { scrollTop, scrollHeight, clientHeight } = evt.target;
        cguCanBeValidated = scrollTop + clientHeight >= scrollHeight - 100;
      }}
    >
      <StaticMarkdown content={data.content} />
    </div>

    <div class="text-right">
      <LinkButton
        label="Refuser et me déconnecter"
        secondary
        to="/auth/deconnexion"
        extraClass="!border-error !text-error hover:!text-white hover:border-error hover:!bg-error"
      />
      <Button
        type="submit"
        label="Valider et accéder à DORA"
        on:click={doAcceptCgu}
        disabled={!cguCanBeValidated}
      />
    </div>
  </CenteredGrid>
</EnsureLoggedIn>

<style type="postcss">
  :global(.cgu h1) {
    @apply text-f32;
  }
  :global(.cgu h2) {
    @apply text-f16;
  }
  :global(.cgu p, .cgu li, .cgu a) {
    @apply text-f14;
  }
  :global(.cgu .prose) {
    @apply max-w-none;
  }
</style>
