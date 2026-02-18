<script lang="ts">
  import { page } from "$app/state";

  import PcButton from "$lib/components/specialized/pc-button.svelte";

  import { getNextPage } from "../../auth/utils";
  import MenuInscriptionBase from "./menu-inscription-base.svelte";

  const nextPage = getNextPage(page.url);
</script>

<MenuInscriptionBase
  text="Pour accéder à votre portail, vous devez avoir un compte ProConnect."
>
  <div class="mb-s16">
    <PcButton {nextPage} noHelpSection />
  </div>
</MenuInscriptionBase>
