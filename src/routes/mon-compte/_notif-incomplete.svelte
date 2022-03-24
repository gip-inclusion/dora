<script>
  import LinkButton from "$lib/components/link-button.svelte";
  import Notice from "$lib/components/notice.svelte";
</script>

<Notice title="Informations incomplètes" type="error">
  <p class="text-f14">
    Complétez votre compte afin de pouvoir utiliser toutes les fonctionnalités
    de DORA.
  </p>

  <LinkButton
    label="Modifier…"
    to="/mon-compte/editer"
    small
    secondary
    slot="button"
  />
</Notice>
