<script lang="ts">
  import type { Service, ShortService } from "$lib/types";
  import ContactEmail from "../../contact-email.svelte";
  import ContactPhone from "../../contact-phone.svelte";

  export let service: Service | ShortService;
  export let useWhiteText = false;
</script>

<div>
  <div class="flex flex-col gap-s4 text-f14" class:text-white={useWhiteText}>
    {#if service.contactName}
      <p class="mb-s6 mr-s24 text-gray-dark" class:text-white={useWhiteText}>
        <strong>{service.contactName}</strong>
      </p>
    {/if}
    <ContactEmail {service} preferred />
    <ContactPhone {service} preferred />
  </div>
</div>
