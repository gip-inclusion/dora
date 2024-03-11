<script lang="ts">
  import logoIC from "$lib/assets/inclusion-connect/logo-inclusion-connect.svg";

  export let nextPage: string;
  export let loginHint: string = "";
</script>

<div class="text-center">
  <a
    class="mb-s24 inline-block"
    href="/auth/ic-connect?next={encodeURIComponent(nextPage)}{loginHint}"
  >
    <div
      class="mx-auto mt-s24 flex items-center justify-center rounded-full bg-france-blue p-s6 pr-s24 text-f16 text-white transition-colors hover:bg-[#2323FF]"
    >
      <span class="h-[62px] w-[62px] rounded-full bg-white p-s6">
        <img src={logoIC} alt="" class="max-w-none" />
      </span>
      <div class="ml-s16 text-left">
        S’identifier avec <strong class="whitespace-nowrap">
          Inclusion Connect
        </strong>
      </div>
    </div>
  </a>

  <div class="text-center">
    <a
      class="text-magenta-cta underline"
      target="_blank"
      title="Ouverture dans une nouvelle fenêtre"
      rel="noopener"
      href="https://aide.dora.inclusion.beta.gouv.fr/fr/category/inscription-et-gestion-du-compte-ha8m5b/"
    >
      Besoin d’aide&nbsp;? Contactez-nous
    </a>
  </div>
</div>
