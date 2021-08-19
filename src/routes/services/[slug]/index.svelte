<script context="module">
  import { getService } from "$lib/services";
  import { getStructure } from "$lib/structures";

  export async function load({ page, _fetch, _session, _context }) {
    const service = (await getService(`${page.params.slug}`)).props.service;
    const structure = (await getStructure(service.structure)).props.structure;
    return {
      props: {
        service,
        structure,
      },
    };
  }
</script>

<script>
  import { page } from "$app/stores";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  export let service, structure;

  const editLink = `${$page.path}/edit`;
</script>

<svelte:head>
  <title>Dora: {service.name}</title>
</svelte:head>

<CenteredGrid>
  <div class="col-start-1 col-span-full">
    <h1>{service.name}</h1>
    <LinkButton type="submit" to={editLink} label="Éditer" />
    <strong>id : </strong>{service.id} <br />
    <strong>name : </strong>{service.name} <br />
    <strong>shortDesc : </strong>{service.shortDesc} <br />
    <strong>fullDesc : </strong>{service.fullDesc} <br />
    <strong>kinds : </strong>{service.kinds} <br />
    <strong>categories : </strong>{service.categories} <br />
    <strong>subcategories : </strong>{service.subcategories} <br />
    <strong>isCommonLaw : </strong>{service.isCommonLaw} <br />
    <strong>isCumulative : </strong>{service.isCumulative} <br />
    <strong>hasFee : </strong>{service.hasFee} <br />
    <strong>feeDetails : </strong>{service.feeDetails} <br />
    <strong
      >beneficiariesAccessModes :
    </strong>{service.beneficiariesAccessModes}
    <br />
    <strong
      >beneficiariesAccessModesOther :
    </strong>{service.beneficiariesAccessModesOther} <br />
    <strong>coachOrientationModes : </strong>{service.coachOrientationModes}
    <br />
    <strong
      >coachOrientationModesOther :
    </strong>{service.coachOrientationModesOther}
    <br />
    <strong>forms : </strong>
    <ul>
      {#each service.formsInfo as form}
        <li><a class="underline" href={form.url}>{form.name}</a></li>
      {/each}
    </ul>
    <strong>onlineForm : </strong>{service.onlineForm} <br />
    <strong>contactName : </strong>{service.contactName} <br />
    <strong>contactPhone : </strong>{service.contactPhone} <br />
    <strong>contactEmail : </strong>{service.contactEmail} <br />
    <strong>contactUrl : </strong>{service.contactUrl} <br />
    <strong>isContactInfoPublic : </strong>{service.isContactInfoPublic} <br />
    <strong>locationKind : </strong>{service.locationKind} <br />
    <strong>remoteUrl : </strong>{service.remoteUrl} <br />
    <strong>address1 : </strong>{service.address1} <br />
    <strong>address2 : </strong>{service.address2} <br />
    <strong>postalCode : </strong>{service.postalCode} <br />
    <strong>cityCode : </strong>{service.cityCode} <br />
    <strong>city : </strong>{service.city} <br />
    <strong>longitude : </strong>{service.longitude} <br />
    <strong>latitude : </strong>{service.latitude} <br />
    <strong>isTimeLimited : </strong>{service.isTimeLimited} <br />
    <strong>startDate : </strong>{service.startDate} <br />
    <strong>endDate : </strong>{service.endDate} <br />
    <strong>recurrence : </strong>{service.recurrence} <br />
    <strong>recurrenceOther : </strong>{service.recurrenceOther} <br />
    <strong>suspensionCount : </strong>{service.suspensionCount} <br />
    <strong>suspensionDate : </strong>{service.suspensionDate} <br />
    <strong>creationDate : </strong>{service.creationDate} <br />
    <strong>modificationDate : </strong>{service.modificationDate} <br />
    <strong>structure : </strong>{service.structure} <br />
    <strong>creator : </strong>{service.creator} <br />
    <strong>lastEditor : </strong>{service.lastEditor} <br />
    <strong>accessConditions : </strong>{service.accessConditions} <br />
    <strong>concernedPublic : </strong>{service.concernedPublic} <br />
    <strong>requirements : </strong>{service.requirements} <br />
    <strong>credentials : </strong>{service.credentials} <br />
  </div>
</CenteredGrid>
