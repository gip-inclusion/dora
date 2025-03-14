<script lang="ts">
  import type { Model, Service } from "$lib/types";
  import { formatFilePath } from "$lib/utils/file";

  export let service: Service | Model;

  $: hasDocuments =
    (Array.isArray(service.formsInfo) && service.formsInfo.length > 0) ||
    service.onlineForm;
  $: hasCredentials =
    Array.isArray(service.credentialsDisplay) &&
    service.credentialsDisplay.length > 0;
</script>

{#if hasDocuments || hasCredentials}
  <section class="gap-s24 flex flex-col">
    <h2 class="text-f23 text-france-blue mb-s0 leading-32 font-bold">
      Les documents à fournir
    </h2>
    {#if hasDocuments}
      <section>
        <h3 class="text-f17 leading-s24 text-gray-dark mb-s8 font-bold">
          Documents à compléter
        </h3>
        <ul class="text-gray-text space-y-s2 list-inside list-disc">
          {#if Array.isArray(service.formsInfo)}
            {#each service.formsInfo as form}
              <li>
                <a
                  class="underline"
                  target="_blank"
                  href={form.url}
                  title="Ouverture dans une nouvelle fenêtre"
                  rel="noopener ugc">{formatFilePath(form.name)}</a
                >
              </li>
            {/each}
          {/if}
          {#if service.onlineForm}
            <li>
              <a
                class="underline"
                target="_blank"
                href={service.onlineForm}
                title="Ouverture dans une nouvelle fenêtre"
                rel="noopener ugc">{service.onlineForm}</a
              >
            </li>
          {/if}
        </ul>
      </section>
    {/if}
    {#if hasCredentials}
      <section>
        <h3 class="text-f17 leading-s24 text-gray-dark mb-s8 font-bold">
          Justificatifs à fournir
        </h3>
        <ul class="text-gray-text space-y-s2 list-inside list-disc">
          {#each service.credentialsDisplay as creds}
            <li>{creds}</li>
          {/each}
        </ul>
      </section>
    {/if}
  </section>
{/if}
