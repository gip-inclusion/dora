<script>
  import OrientationBox from "./service-orientation.svelte";
  import ServicePresentation from "./service-presentation.svelte";
  import { addlinkToUrls, shortenString } from "$lib/utils";
  import Tag from "$lib/components/tag.svelte";

  export let service;
  export let isModel = false;
</script>

<div class="flex flex-col gap-s24 lg:flex-row">
  <div class="lg:w-2/3">
    <div class="mb-s12 flex flex-wrap gap-s8">
      {#each service.categoriesDisplay.sort( (a, b) => a.localeCompare( b, "fr", { numeric: true } ) ) as categoryDisplay}
        <Tag bgColorClass="bg-magenta-brand" textColorClass="text-white"
          >{categoryDisplay}</Tag
        >
      {/each}
      {#if service.isCumulative}
        <Tag bgColorClass="bg-info" textColorClass="text-white"
          >Service cumulable</Tag
        >
      {:else}
        <Tag bgColorClass="bg-warning" textColorClass="text-white"
          >Service non cumulable</Tag
        >
      {/if}
      {#if service.hasFee}
        <Tag bgColorClass="bg-warning" textColorClass="text-white"
          >Frais à charge du bénéficiaire</Tag
        >
      {/if}
      {#if !isModel && service.locationKinds.includes("a-distance")}
        <Tag bgColorClass="bg-info" textColorClass="text-white">À distance</Tag>
      {/if}
    </div>
    <p class="text-f12 text-gray-text-alt">
      {service.kindsDisplay.join(", ")}
    </p>

    <p class="text-f18"><strong>{service.shortDesc}</strong></p>
  </div>

  <div class="lg:w-1/3">
    {#if !isModel && service.locationKinds.length}
      {#if service.locationKinds.includes("en-presentiel")}
        <h4>En présentiel</h4>
        <p class="pb-s16 text-f14">
          {service.address1}<br />
          {#if service.address2}{service.address2}<br />{/if}
          {service.postalCode}
          {service.city}
        </p>
      {/if}
      {#if service.locationKinds.includes("a-distance")}
        <strong>À distance</strong>
        <p class="pb-s16 text-f14">
          <a target="_blank" rel="noopener nofollow" href={service.remoteUrl}>
            {shortenString(service.remoteUrl, 35)}
          </a>
        </p>
      {/if}
    {/if}

    {#if service.recurrence}
      <h4>Fréquence et horaires</h4>
      <p class="text-f14">{service.recurrence}</p>
    {/if}
  </div>
</div>

<div class="break-word flex flex-col gap-s24 lg:flex-row">
  <div class="lg:w-2/3">
    <div class="mb-s48 flex flex-col gap-s32 lg:flex-row">
      <div class="flex-1">
        <h2>Publics</h2>

        <h4>Profils</h4>
        <ul class="mb-s24 list-outside list-disc pl-s20 text-f14">
          {#each service.concernedPublicDisplay as pub}
            <li><span>{pub}</span></li>
          {:else}
            <li><span>Tout le monde</span></li>
          {/each}
        </ul>

        <h4>Critères</h4>
        <ul class="mb-s24 list-outside list-disc pl-s20 text-f14">
          {#each service.accessConditionsDisplay as condition}
            <li><span>{condition}</span></li>
          {:else}
            <li><span>Aucun</span></li>
          {/each}
          {#if service.qpvOrZrr && !service.isModel}
            <li>uniquement QPV + ZRR</li>
          {/if}
        </ul>

        <h4>Pré-requis, compétences</h4>
        <ul class="mb-s24 list-outside list-disc pl-s20 text-f14">
          {#each service.requirementsDisplay as reqs}
            <li><span>{reqs}</span></li>
          {:else}
            <li><span>Aucun</span></li>
          {/each}
        </ul>
      </div>
      <div class="flex-1">
        <h2>Modalités</h2>
        <h4>Pour l'accompagnateur</h4>
        <ul class="mb-s24 list-outside list-disc pl-s20 text-f14">
          {#each service.coachOrientationModesDisplay as mode}
            <li>
              {#if mode === "Autre (préciser)"}
                {@html addlinkToUrls(service.coachOrientationModesOther)}
              {:else}
                {mode}
              {/if}
            </li>
          {:else}
            <li><span>Non renseigné</span></li>
          {/each}
        </ul>

        <h4>Pour le bénéficiaire</h4>
        <ul class="mb-s24 list-outside list-disc pl-s20 text-f14">
          {#each service.beneficiariesAccessModesDisplay as mode}
            <li>
              {#if mode === "Autre (préciser)"}
                {@html addlinkToUrls(service.beneficiariesAccessModesOther)}
              {:else}
                {mode}
              {/if}
            </li>
          {:else}
            <li><span>Non renseigné</span></li>
          {/each}
        </ul>

        {#if service.hasFee}
          <div class="mb-s24">
            <h4>Frais</h4>

            <p class="text-f14">{service.feeDetails}</p>
          </div>
        {/if}
      </div>
    </div>
  </div>

  <div class="lg:w-1/3">
    <div
      class="mb-s24 rounded-md border border-gray-00 px-s24 pt-s24 shadow-md"
    >
      <h4>Justificatifs</h4>
      <ul class="mb-s24 list-outside list-disc pl-s20 text-f14">
        {#each service.credentialsDisplay as creds}
          <li><span>{creds}</span></li>
        {:else}
          <li><span>Aucun</span></li>
        {/each}
      </ul>

      {#if service.formsInfo.length || service.onlineForm}
        <h4>À compléter</h4>
        <ul class="mb-s24 list-outside list-disc pl-s20 text-f14">
          {#each service.formsInfo as form}
            <li>
              <span class="break-word">
                <a target="_blank" rel="noopener nofollow" href={form.url}
                  >{form.name}</a
                >
              </span>
            </li>
          {/each}
          {#if service.onlineForm}
            <li>
              <span class="break-word">
                <a
                  target="_blank"
                  rel="noopener nofollow"
                  href={service.onlineForm}>{service.onlineForm}</a
                >
              </span>
            </li>
          {/if}
        </ul>
      {/if}
      {#if !isModel}
        <OrientationBox {service} />
      {/if}
    </div>
  </div>
</div>

{#if service.fullDesc}
  <div class="mb-s48 lg:w-2/3">
    <ServicePresentation {service} />
  </div>
{/if}
