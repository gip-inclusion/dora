<script>
  import NewsletterButton from "$lib/components/newsletter-button.svelte";
</script>

<div class="bg-gray-bg p-s24">
  <div class="m-auto max-w-7xl items-center justify-between lg:flex lg:px-s32">
    <div class="items-center lg:flex lg:flex-row">
      <h2 class="m-s0 text-f14 text-gray-dark">Infolettre</h2>
      <span class="hidden lg:inline">&nbsp;•&nbsp;</span>
      <p class="m-s0 text-f14">
        Une fois par mois, recevez un courriel pour être informé des évolutions
        de DORA.
      </p>
    </div>
    <div class="mt-s24 text-center lg:mt-s0">
      <NewsletterButton
        extraClass="!border-0 !bg-transparent hover:!text-magenta-cta hover:!underline"
      />
    </div>
  </div>
</div>
