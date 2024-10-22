<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { userInfo } from "$lib/utils/auth";

  export let model;

  export let readOnly = true;
</script>

<div class="flex flex-col items-end">
  {#if !readOnly}
    <LinkButton
      label="Modifier"
      to="/modeles/{model.slug}/editer"
      small
      noBackground
    />
  {/if}

  {#if $userInfo}
    <LinkButton
      label="Créer un service"
      small
      to={`/services/creer?modele=${model.slug}`}
      noBackground
    />
  {/if}
</div>
