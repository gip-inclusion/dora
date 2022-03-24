<script>
  import LinkButton from "$lib/components/link-button.svelte";
  import Notice from "$lib/components/notice.svelte";
</script>

<Notice title="Aidez-nous à améliorer DORA">
  <p class="text-f14">
    Partagez votre expérience, des problèmes que vous rencontrez ou des
    propositions d’amélioration.
  </p>

  <LinkButton
    to="https://itou.typeform.com/to/DPQOe5pP"
    label="Participer (3min.)…"
    otherTab
    nofollow
    small
    secondary
    slot="button"
  />
</Notice>
