<script lang="ts">
  import LinkButton from "#lib/components/display/link-button.svelte";
  import type { Model } from "#lib/types.js";
  import { userInfo } from "#lib/utils/auth.js";

  interface Props {
    model: Model;
    readOnly?: boolean;
  }

  let { model, readOnly = true }: Props = $props();
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
