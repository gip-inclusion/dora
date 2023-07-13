<script lang="ts">
  import Accordion from "$lib/components/display/accordion.svelte";
  import type { Service } from "$lib/types";
  import { addlinkToUrls } from "$lib/utils/misc";
  import { formatFilePath } from "$lib/utils/file";

  export let service: Service;
</script>

<div id="orientation-modes">
  <Accordion title="Comment mobiliser ce service ?">
    <div class="mb-s32">
      <h3>Les démarches à réaliser</h3>

      <h4>Pour les accompagnateurs</h4>
      <ul>
        {#each service.coachOrientationModesDisplay as mode (mode)}
          <li>
            {#if mode === "Autre (préciser)"}
              {@html addlinkToUrls(service.coachOrientationModesOther)}
            {:else}
              {mode}
            {/if}
          </li>
        {:else}
          <li>Non renseigné</li>
        {/each}
      </ul>

      <h4>Pour les bénéficiaires</h4>
      <ul>
        {#each service.beneficiariesAccessModesDisplay as mode (mode)}
          <li>
            {#if mode === "Autre (préciser)"}
              {@html addlinkToUrls(service.beneficiariesAccessModesOther)}
            {:else}
              {mode}
            {/if}
          </li>
        {:else}
          <li>Non renseigné</li>
        {/each}
      </ul>
    </div>

    <div class="mb-s32">
      <h3>Les documents à fournir</h3>

      <h4>Documents à compléter</h4>
      <ul>
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
        {#if service.formsInfo.length === 0 && !service.onlineForm}
          <li>Aucun</li>
        {/if}
      </ul>

      <h4>Justificatifs à fournir</h4>
      <ul>
        {#each service.credentialsDisplay as creds}
          <li><span>{creds}</span></li>
        {:else}
          <li><span>Aucun</span></li>
        {/each}
      </ul>
    </div>
  </Accordion>
</div>

<style lang="postcss">
  ul {
    @apply mb-s24 list-disc break-all pl-s20 text-f18 leading-32 text-gray-text;
  }
</style>
