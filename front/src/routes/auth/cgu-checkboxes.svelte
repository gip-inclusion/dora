<script lang="ts">
  import CheckboxMark from "$lib/components/display/checkbox-mark.svelte";

  interface Props {
    cguAccepted: boolean;
    coResponsibilityAccepted: boolean;
    showCoResponsibilityCheckbox: boolean;
  }

  let {
    cguAccepted = $bindable(),
    coResponsibilityAccepted = $bindable(),
    showCoResponsibilityCheckbox,
  }: Props = $props();
</script>

{#if showCoResponsibilityCheckbox}
  <div class="legend mb-s16">
    <label class="flex flex-row items-start">
      <input
        bind:checked={coResponsibilityAccepted}
        type="checkbox"
        class="hidden"
      />
      <CheckboxMark />
      <span class="ml-s16 text-f14 text-gray-text inline-block">
        Je déclare être habilité à engager la responsabilité de ma structure en
        acceptant l’accord de responsabilité conjointe présent dans les
        <a
          href="/cgu#accord_co_responsabilite"
          class="underline"
          target="_blank"
          rel="noopener">Conditions générales d’utilisation</a
        >
      </span></label
    >
  </div>
{/if}
<div class="legend">
  <label class="flex flex-row items-start">
    <input bind:checked={cguAccepted} type="checkbox" class="hidden" />
    <CheckboxMark />
    <span class="ml-s16 text-f14 text-gray-text inline-block">
      Je déclare accepter les
      <a href="/cgu" class="underline" target="_blank" rel="noopener"
        >Conditions générales d’utilisation</a
      > et faire partie de la structure mentionnée ci-dessus.</span
    >
  </label>
</div>
