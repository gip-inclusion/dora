<script lang="ts">
  import Accordion from "$lib/components/display/accordion.svelte";

  import type { Model, Service } from "$lib/types";
  import { formatFilePath } from "$lib/utils/file";

  export let service: Service | Model;
</script>

<div id="orientation-modes">
  <Accordion title="Comment mobiliser ce service ?">
    <div class="mb-s32">
      <h3>Les documents à fournir</h3>

      <h4>Documents à compléter</h4>
      <ul class="typographic-list">
        {#if Array.isArray(service.formsInfo)}
          {#each service.formsInfo as form}
            <li>
              <span class="break-word">
                <a
                  target="_blank"
                  rel="noopener ugc"
                  href={form.url}
                  class="hover:underline"
                  title="Ouverture dans une nouvelle fenêtre"
                  >{formatFilePath(form.name)}</a
                >
              </span>
            </li>
          {/each}
        {/if}
        {#if service.onlineForm}
          <li>
            <span class="break-word">
              <a
                target="_blank"
                class="hover:underline"
                rel="noopener ugc"
                title="Ouverture dans une nouvelle fenêtre"
                href={service.onlineForm}>{service.onlineForm}</a
              >
            </span>
          </li>
        {/if}
        {#if Array.isArray(service.formsInfo)}
          {#if service.formsInfo.length === 0 && !service.onlineForm}
            <li>Aucun</li>
          {/if}
        {:else if !service.onlineForm}
          <li>Non renseigné</li>
        {/if}
      </ul>

      <h4>Justificatifs à fournir</h4>
      <ul class="typographic-list">
        {#if Array.isArray(service.credentialsDisplay)}
          {#each service.credentialsDisplay as creds}
            <li><span>{creds}</span></li>
          {:else}
            <li><span>Aucun</span></li>
          {/each}
        {:else}
          <li>Non renseigné</li>
        {/if}
      </ul>
    </div>
  </Accordion>
</div>

<style lang="postcss">
  @reference "../../../../app.css";

  .typographic-list {
    @apply mb-s24 pl-s20 text-f18 text-gray-text list-disc leading-32 break-all;
  }
</style>
