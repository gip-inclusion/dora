<script lang="ts">
  import type { Model, Service } from "$lib/types";
  import { formatFilePath } from "$lib/utils/file";

  import ServiceList from "./components/service-list.svelte";
  import ServiceSection from "./components/service-section.svelte";
  import ServiceSubsection from "./components/service-subsection.svelte";

  export let service: Service | Model;

  $: hasDocuments =
    (Array.isArray(service.formsInfo) && service.formsInfo.length > 0) ||
    service.onlineForm;
  $: hasCredentials =
    Array.isArray(service.credentialsDisplay) &&
    service.credentialsDisplay.length > 0;
</script>

{#if hasDocuments || hasCredentials}
  <ServiceSection title="Les documents à fournir">
    {#if hasDocuments}
      <ServiceSubsection title="Documents à compléter">
        <ServiceList>
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
        </ServiceList>
      </ServiceSubsection>
    {/if}
    {#if hasCredentials}
      <ServiceSubsection title="Justificatifs à fournir">
        <ServiceList>
          {#each service.credentialsDisplay as creds}
            <li>{creds}</li>
          {/each}
        </ServiceList>
      </ServiceSubsection>
    {/if}
  </ServiceSection>
{/if}
