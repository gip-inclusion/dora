<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Notice from "$lib/components/display/notice.svelte";
</script>

<Notice title="Aidez-nous à améliorer DORA">
  <p class="text-f14">
    Partagez votre expérience, des problèmes que vous rencontrez ou des
    propositions d’amélioration.
  </p>

  <LinkButton
    to="https://tally.so/r/mVLr7J?source=tdbuser"
    label="Participer"
    otherTab
    nofollow
    small
    secondary
    slot="button"
  />
</Notice>
