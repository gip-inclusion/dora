<script lang="ts">
  import {
    consent,
    type ConsentChoices,
    type ConsentKey,
  } from "$lib/utils/consent.svelte";

  interface Props {
    handleSavePreferences: (consentChoices: ConsentChoices) => void;
    handleBackClick: () => void;
  }

  let { handleSavePreferences, handleBackClick }: Props = $props();

  let consentChoices: ConsentChoices = { ...consent.consentChoices };

  function toggleConsentByKey(key: ConsentKey) {
    consentChoices[key] = !consentChoices[key];
  }
</script>

<div>
  <p class="mb-6 leading-relaxed text-gray-600">
    Choose which cookies you want to allow:
  </p>

  <div class="mb-6">
    <div class="mb-3 rounded border border-gray-200 p-4">
      <label class="flex cursor-pointer items-start gap-4">
        <input
          type="checkbox"
          class="mt-1 cursor-pointer"
          checked={consentChoices.matomo}
          on:change={() => toggleConsentByKey("matomo")}
        />
        <div>
          <strong class="mb-1 block">Matomo Analytics</strong>
          <span class="text-sm text-gray-500"
            >Help us understand how you use our site</span
          >
        </div>
      </label>
    </div>

    <div class="mb-3 rounded border border-gray-200 p-4">
      <label class="flex cursor-pointer items-start gap-4">
        <input
          type="checkbox"
          class="mt-1 cursor-pointer"
          checked={consentChoices.googleCSE}
          on:change={() => toggleConsentByKey("googleCSE")}
        />
        <div>
          <strong class="mb-1 block">Google Custom Search</strong>
          <span class="text-sm text-gray-500"
            >Enhanced search functionality</span
          >
        </div>
      </label>
    </div>

    <div class="mb-3 rounded border border-gray-200 p-4">
      <label class="flex cursor-pointer items-start gap-4">
        <input
          type="checkbox"
          class="mt-1 cursor-pointer"
          checked={consentChoices.crisp}
          on:change={() => toggleConsentByKey("crisp")}
        />
        <div>
          <strong class="mb-1 block">Crisp Chat</strong>
          <span class="text-sm text-gray-500">Live customer support chat</span>
        </div>
      </label>
    </div>
  </div>

  <div class="flex flex-wrap gap-3">
    <button
      class="cursor-pointer rounded bg-blue-600 px-6 py-3 text-base text-white transition-all duration-200 hover:bg-blue-700"
      on:click={() => handleSavePreferences(consentChoices)}
    >
      Save Preferences
    </button>
    <button
      class="cursor-pointer rounded bg-transparent px-6 py-3 text-base text-blue-600 underline transition-all duration-200 hover:text-blue-700"
      on:click={handleBackClick}
    >
      Back
    </button>
  </div>
</div>
