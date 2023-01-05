<script lang="ts">
  import { newspaperIcon } from "$lib/icons";
  import LinkButton from "../display/link-button.svelte";
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
      <LinkButton
        label="S’abonner à l’infolettre"
        icon={newspaperIcon}
        iconOnRight
        secondary
        extraClass="!border-0 !bg-transparent hover:!text-magenta-cta hover:!underline"
        to="https://d4c653e7.sibforms.com/serve/MUIEAEkY4naptXBIq5NdRg5UPxP1wmwbGCinne5c1gynY-wfrZ0Dz0QP_NqkXtfyYqhdaq3AO8VFZJ9giRi9ZT0eah7Ut2U0LeKSTVIHQb_5nhvTLUMWXo9ZMeIYCHVlzmjkXGQ66S5ewcYpSADUgV--2RVZ_mrnsRJQoCNwZ8y-sWzfQsEzfKuTA7SLbZ_dWeqaigudym3EaiHT"
        otherTab
        nofollow
      />
    </div>
  </div>
</div>
