<script lang="ts">
  import { phoneLineIcon } from "$lib/icons";
  import { formatPhoneNumber } from "$lib/utils/misc";

  export let service;
  export let preferred = false;
</script>

<div class="mb-s6 mr-s24">
  <a
    class="flex items-center text-f16"
    class:font-bold={preferred}
    href="tel:{service.contactPhone}"
  >
    <span
      class="mr-s8 h-s24 w-s24 fill-current"
      aria-label="Numéro de téléphone"
    >
      {@html phoneLineIcon}
    </span>
    {formatPhoneNumber(service.contactPhone)}
  </a>
</div>
