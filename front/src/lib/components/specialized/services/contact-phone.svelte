<script lang="ts">
  import PhoneLineDevice from "svelte-remix/PhoneLineDevice.svelte";

  import { formatPhoneNumber } from "#lib/utils/misc.ts";

  interface Props {
    phoneNumber: string;
    preferred?: boolean;
  }

  let { phoneNumber, preferred = false }: Props = $props();
</script>

<div class="mb-s6 mr-s24">
  <a
    class="text-f16 flex items-center"
    class:font-bold={preferred}
    href="tel:{phoneNumber}"
  >
    <span
      class="mr-s8 h-s24 w-s24 fill-current"
      role="img"
      aria-label="Numéro de téléphone"
    >
      <PhoneLineDevice />
    </span>
    {formatPhoneNumber(phoneNumber)}
  </a>
</div>
