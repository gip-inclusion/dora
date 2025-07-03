<script lang="ts">
  import { fly } from "svelte/transition";

  import CheckLineSystem from "svelte-remix/CheckLineSystem.svelte";
  import FileCopyLineDocument from "svelte-remix/FileCopyLineDocument.svelte";

  import type { Model, Service } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";

  import ServiceSection from "./components/service-section.svelte";

  interface Props {
    service: Service | Model;
  }

  let { service }: Props = $props();

  let isDI = $derived("source" in service);
  let showComponent = $derived($userInfo?.isStaff && !service.isModel && isDI);
  let info = $derived(service.isModel
    ? []
    : [
        {
          label: "Source",
          value: service.source as string, // toujours string car c’est un service DI
        },
        {
          label: "Identifiant de structure",
          value: service.structure,
        },
      ]);

  let copiedIndex: number | null = $state(null);

  function handleCopy(value: string, index: number) {
    navigator.clipboard.writeText(value);
    copiedIndex = index;
    setTimeout(() => (copiedIndex = null), 2000);
  }
</script>

{#if showComponent}
  <ServiceSection title="Informations d’identification de structure DI">
    <ul>
      {#each info as item, index}
        <li class="gap-s4 flex items-center">
          {item.label}&#8239;:
          <code class="border-gray-02 px-s8 py-s4 rounded-md border"
            >{item.value}</code
          ><button
            class="text-magenta-brand"
            onclick={() => handleCopy(item.value, index)}
          >
            <div class="w-s24 h-s24 relative">
              {#if copiedIndex === index}
                <div class="absolute" transition:fly={{ y: 50, duration: 500 }}>
                  <CheckLineSystem />
                </div>
              {:else}
                <div class="absolute" transition:fly={{ y: 50, duration: 500 }}>
                  <FileCopyLineDocument />
                </div>
              {/if}
            </div>
          </button>
        </li>
      {/each}
    </ul>
  </ServiceSection>
{/if}
