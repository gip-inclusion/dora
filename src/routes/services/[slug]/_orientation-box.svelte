<script>
  import { page } from "$app/stores";
  import { token } from "$lib/auth";
  import Button from "$lib/components/button.svelte";
  import Field from "$lib/components/forms/field.svelte";

  export let service, structure;

  export let url = `https://${$page.host}${$page.path}`;
</script>

<style>
  .wrapper {
    position: relative;
    top: -4rem;
    display: flex flex-col;
    padding: var(--s32);
    border: 4px solid var(--col-gray-dark);
    margin-right: auto;
    margin-left: auto;
    background-color: var(--col-white);
    border-radius: var(--s4);
  }
</style>

<div class="wrapper">
  <h3>Orientez votre bénéficiaire</h3>
  Vous devez être connecté•e pour accéder aux informations de contact et orienter
  votre bénéficiaire.
  <Button label="Orientez votre bénéficiaire" disabled={!$token} />
  <div class="text-xs">
    {#if $token}
      <strong>Formulaires uploadés : </strong><br />
      <ul>
        {#each service.formsInfo as form}
          <li><a class="underline" href={form.url}>{form.name}</a></li>
        {/each}
      </ul>
      <strong>Formulaire en ligne : </strong>{service.onlineForm}<br />
      <strong>Nom du contact : </strong>{service.contactName}<br />
      <strong>Tel du contact : </strong>{service.contactPhone}<br />
      <strong>Email du contact : </strong>{service.contactEmail}<br />
      <strong>Lien visio : </strong>{service.remoteUrl}<br />
      <strong>Adresse : </strong>{service.address1}<br />
      <strong>Complément adresse : </strong>{service.address2}<br />
      <strong>
        Comment orienter un bénéficiaire en tant qu’accompagnateur :<br />
      </strong>
      {service.coachOrientationModesDisplay}<br />
      <strong>
        Modalité d'accompagnement :
      </strong>{service.coachOrientationModesOther}<br />
    {/if}
  </div>
  <div class="mt-2">
    <Field
      type="text"
      label="Partagez cette offre"
      value={url}
      vertical
      readonly />
  </div>
</div>

<!--
    <strong>Formulaires uploadés : </strong>
    <ul>
      {#each service.formsInfo as form}
        <li><a class="underline" href={form.url}>{form.name}</a></li>
      {/each}
    </ul>
    <strong>Formulaire en ligne : </strong>{service.onlineForm}
    <strong>Nom du contact : </strong>{service.contactName}
    <strong>Tel du contact : </strong>{service.contactPhone}
    <strong>Email du contact : </strong>{service.contactEmail}
    <strong>Lien visio : </strong>{service.remoteUrl}
    <strong>Adresse : </strong>{service.address1}
    <strong>Complément adresse : </strong>{service.address2}
    <strong>
      Comment orienter un bénéficiaire en tant qu’accompagnateur :
    </strong>
      {service.coachOrientationModesDisplay}
    <strong>
      Modalité d'accompagnement :
    </strong>{service.coachOrientationModesOther}
 -->
