<script lang="ts">
  import PhoneLineDevice from "svelte-remix/PhoneLineDevice.svelte";

  import type { Service, ShortService } from "$lib/types";
  import { formatPhoneNumber } from "$lib/utils/misc";

  interface Props {
    service: Service | ShortService;
    preferred?: boolean;
  }

  let { service, preferred = false }: Props = $props();
</script>

<div class="mb-s6 mr-s24">
  <a
    class="text-f16 flex items-center"
    class:font-bold={preferred}
    href="tel:{service.contactPhone}"
  >
    <span
      class="mr-s8 h-s24 w-s24 fill-current"
      role="img"
      aria-label="Numéro de téléphone"
    >
      <PhoneLineDevice />
    </span>
    {formatPhoneNumber(service.contactPhone)}
  </a>
</div>
