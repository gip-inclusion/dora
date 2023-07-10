<script lang="ts">
  import ContactEmail from "$lib/components/specialized/services/contact-email.svelte";
  import ContactPhone from "$lib/components/specialized/services/contact-phone.svelte";

  export let service;
</script>

<div class="block rounded-ml border border-gray-02 p-s24 px-s32">
  <h3 class="text-france-blue">Contact</h3>
  <p class="text-f16">
    En cas de doute, vous pouvez contacter la personne responsable du
    service&nbsp;:
  </p>
  <div class="flex flex-col gap-s4">
    {#if service.contactName}
      <p class="mb-s6 mr-s24 text-f17 text-gray-dark">
        <strong>{service.contactName}</strong>
      </p>
    {/if}
    <ContactPhone {service} />
    <ContactEmail {service} />
  </div>
</div>
