<script lang="ts">
  import type { Service } from "$lib/types";
  import { phoneLineIcon } from "$lib/icons";
  import { formatPhoneNumber } from "$lib/utils/misc";

  export let service: Service;
  export let preferred = false;

  const displayContact = service.contactEmail || service.contactPhone;
</script>

{#if displayContact}
  <div class="mb-s6 mr-s24">
    <a
      class="flex items-center text-f16"
      class:font-bold={preferred}
      href="tel:{service.contactPhone}"
    >
      <span
        class="mr-s8 h-s24 w-s24 fill-current"
        role="img"
        aria-label="Numéro de téléphone"
      >
        {@html phoneLineIcon}
      </span>
      {formatPhoneNumber(service.contactPhone)}
    </a>
  </div>
{/if}
